import os

import uvicorn
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpoint
from sentence_transformers import SentenceTransformer
from pymongo import MongoClient
from fastapi import FastAPI
from models.request import Request
from models.response import Response

load_dotenv()

app = FastAPI()

client = MongoClient(os.environ["MONGO_URI"])
db = client.festival_database
collection = db.festivals


class FestivalInformationAgent:
    def __init__(self):
        self.model = HuggingFaceEndpoint(repo_id="mistralai/Mistral-7B-Instruct-v0.2", task="text-generation", temperature=0.8)
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

    def get_vector_search_data(self, search_input):
        query_embedding = self.embedding_model.encode(search_input).tolist()

        query_result = list(db.festivals.aggregate([
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": "embedding",
                    "queryVector": query_embedding,
                    "numCandidates": 20,
                    "limit": 10
                }
            }
        ]))

        new_result = [{k: v for k, v in item.items() if k != 'embedding'} for item in query_result]

        return new_result

    def get_festival_information(self, context, question):
        prompt = ChatPromptTemplate.from_template(
            """
            Answer the question based only on the following context: {context}
            Question: {question}
            """
        )

        chain = (
                RunnableParallel({
                    "context": str,
                    "question": RunnablePassthrough()
                })
                | prompt
                | self.model
                | StrOutputParser()
        )

        return chain.invoke({
            "context": context,
            "question": question
        })


@app.post("/", response_model=Response)
def search_festival(request: Request):
    message = request.message

    vector_search = festival_agent.get_vector_search_data(message)
    result = festival_agent.get_festival_information(
        context=vector_search,
        question=message
    )

    return Response(message=result, status_code=200)


if __name__ == "__main__":
    festival_agent = FestivalInformationAgent()
    uvicorn.run(app, host="0.0.0.0")
