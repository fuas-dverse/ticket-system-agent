import os
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpoint
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from agentDVerse.agent import Agent

load_dotenv()

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


def search_festival(x):
    vector_search = festival_agent.get_vector_search_data(x)
    result = festival_agent.get_festival_information(
        context=vector_search,
        question=x
    )

    agent.send_response_to_next(
        initial=x,
        message={
            "message": result
        }
    )


if __name__ == "__main__":
    agent = Agent(
        name="Festival Information Agent",
        description="This agent provides information about upcoming festivals.",
        topics=["festival", "party", "festival-information"],
        output_format="text",
        callback=search_festival
    )

    festival_agent = FestivalInformationAgent()
