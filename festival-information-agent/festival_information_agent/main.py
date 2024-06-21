import os
from dotenv import load_dotenv
from langchain_community.vectorstores.mongodb_atlas import MongoDBAtlasVectorSearch
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableParallel, RunnablePassthrough
from langchain_huggingface import HuggingFaceEndpoint
from langchain_openai import OpenAIEmbeddings

load_dotenv()

MONGO_URI = os.environ.get("MONGO_URI")
DB_NAME = "festival_database"
COLLECTION_NAME = "festivals"
ATLAS_VECTOR_SEARCH_INDEX_NAME = "vector_index"


def get_vector_search_data(search_input):
    vectorstore = MongoDBAtlasVectorSearch.from_connection_string(
        MONGO_URI,
        DB_NAME + "." + COLLECTION_NAME,
        embedding=OpenAIEmbeddings(disallowed_special=(), model="text-embedding-3-small"),
        index_name=ATLAS_VECTOR_SEARCH_INDEX_NAME,
        text_key="name"
    )

    vectorstore = vectorstore.as_retriever(search_kwargs={"k": 5})

    output = vectorstore.get_relevant_documents(search_input)
    for item in output:
        if hasattr(item, "metadata") and "embedding" in item.metadata:
            del item.metadata["embedding"]

        if hasattr(item, "metadata") and "_id" in item.metadata:
            del item.metadata["_id"]

    return output


def get_festival_information(context, question):
    prompt = PromptTemplate.from_template(
        """Answer the question based only on the following context: {context}
        Question: {question}
        Give back the information in a structured JSON format.
        """
    )

    model = HuggingFaceEndpoint(
        repo_id="HuggingFaceH4/zephyr-7b-beta",
        task="text-generation",
        temperature=0.8,
    )

    chain = (
            RunnableParallel({
                "context": str,
                "question": RunnablePassthrough()
            })
            | prompt
            | model
            | StrOutputParser()
    )

    return chain.invoke({
        "context": context,
        "question": question
    })


if __name__ == "__main__":
    user_input = "I want to go festival in Summer. What are the best festivals in Summer? Can you recommend me some based on the price?"

    vector_search = get_vector_search_data(user_input)

    result = get_festival_information(
        context=vector_search,
        question=user_input
    )

    print(result)
