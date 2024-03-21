import json

from bson import json_util
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient
import os

load_dotenv()

open_ai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

client = MongoClient(os.environ["MONGO_URI"])
db = client.festival_database
collection = db.festivals


def vector_search(query_vector):
    result = list(db.festivals.aggregate([
        {
            "$vectorSearch": {
                "index": "vector_index",
                "path": "name_embedding",
                "queryVector": query_vector,
                "numCandidates": 10000,
                "limit": 2
            }
        }
    ]))

    with open('output.json', 'w') as json_file:
        json.dump(result, json_file, default=str)


if __name__ == "__main__":
    vector = name_embedding = open_ai_client.embeddings.create(
            input="asdasdasdad",
            model="text-embedding-3-small",
            dimensions=1536
    ).data[0].embedding

    print(vector)

    vector_search(vector)
