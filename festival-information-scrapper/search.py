import json
import os
from dotenv import load_dotenv
from pymongo import MongoClient

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
                "numCandidates": 3,
                "limit": 3
            }
        }
    ]))

    new_result = [{k: v for k, v in item.items() if k != 'name_embedding'} for item in result]

    with open('output.json', 'w') as json_file:
        json.dump(new_result, json_file, default=str)


if __name__ == "__main__":
    user_input = input("> Enter a search query: ")

    vector = name_embedding = open_ai_client.embeddings.create(
            input=user_input,
            model="text-embedding-3-small",
            dimensions=1536
    ).data[0].embedding

    print(vector)

    vector_search(vector)
