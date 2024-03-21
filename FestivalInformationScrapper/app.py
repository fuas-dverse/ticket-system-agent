import json
import os
from datetime import datetime

import ephem
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from openai import OpenAI
from pymongo import MongoClient

load_dotenv()

open_ai_client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


class Festival:
    def __init__(self, name, description, city, location, latitude, longitude, start_date, end_date, season, price,
                 age, name_embedding):
        self.name = name
        self.description = description
        self.city = city
        self.location = location
        self.latitude = latitude
        self.longitude = longitude
        self.start_date = start_date
        self.end_date = end_date
        self.season = season
        self.price = price
        self.age = age
        self.embeddings = None
        self.name_embedding = None

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "location": self.location,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "season": self.season,
            "price": self.price,
            "age": self.age,
            "name_embedding": self.name_embedding
        }


class FestivalEmbeddings:
    def __init__(self, name_embedding):
        self.name_embedding = name_embedding

    def to_dict(self):
        return {
            "name_embedding": self.name_embedding,
        }


def add_data_to_mongodb(festivals):
    # Connection to MongoDB
    client = MongoClient(os.environ["MONGO_URI"])
    db = client.festival_database
    collection = db.festivals

    collection.delete_many({})

    # Inserting the data
    collection.insert_many(festivals)
    print(f"{len(festivals)} festivals inserted into MongoDB.")


def get_season_from_date(start_date):
    # Convert string to datetime
    start_date = datetime.strptime(start_date, "%Y-%m-%dT%H:%M:%S%z")
    # Convert start_date to a naive datetime object in UTC
    start_date = start_date.replace(tzinfo=None)

    # Calculate the dates of the equinoxes and solstices for the year of start_date
    spring_equinox = ephem.next_vernal_equinox(str(start_date.year)).datetime()
    summer_solstice = ephem.next_summer_solstice(str(start_date.year)).datetime()
    autumn_equinox = ephem.next_autumn_equinox(str(start_date.year)).datetime()
    winter_solstice = ephem.next_winter_solstice(str(start_date.year)).datetime()

    # Determine the season based on the date
    if spring_equinox <= start_date < summer_solstice:
        return "Spring"
    elif summer_solstice <= start_date < autumn_equinox:
        return "Summer"
    elif autumn_equinox <= start_date < winter_solstice:
        return "Autumn"
    else:
        return "Winter"


def scrap_festival_information():
    base_url = "https://festivalfans.nl/agenda/"
    base_page = requests.get(base_url)
    base_soup = BeautifulSoup(base_page.content, "html.parser")
    festival_information_div = base_soup.find_all("div", class_="festival")

    all_festivals = []

    for div in festival_information_div:
        festival_information = div.find("script", {"type": "application/ld+json"})

        for data in festival_information:
            jsn = json.loads(data.string)

            name = jsn.get("name")
            description = jsn.get("description")
            city = jsn.get("location", {}).get("address", {}).get("addressLocality")
            location = jsn.get("location", {}).get("name")
            latitude = jsn.get("location", {}).get("geo", {}).get("latitude")
            longitude = jsn.get("location", {}).get("geo", {}).get("longitude")
            start_date = jsn.get("startDate")
            end_date = jsn.get("endDate")
            price = jsn.get("offers", {}).get("price")

            all_festivals.append(
                Festival(
                    name,
                    description,
                    city,
                    location,
                    latitude,
                    longitude,
                    start_date,
                    end_date,
                    get_season_from_date(start_date),
                    price,
                    None,
                    None
                ).to_dict()
            )

    generate_embedding(all_festivals)
    add_data_to_mongodb(all_festivals)


def generate_embedding(all_festivals):
    for festival in all_festivals:
        name_embedding = open_ai_client.embeddings.create(
            input=[
                festival["name"],
                festival["season"]
            ],
            model="text-embedding-3-small",
            dimensions=1536
        ).data[0].embedding

        festival["name_embedding"] = name_embedding


if __name__ == "__main__":
    scrap_festival_information()
