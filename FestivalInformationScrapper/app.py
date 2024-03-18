import json
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient


class Festival:
    def __init__(self, name, description, city, location, start_date, end_date, price, age):
        self.name = name
        self.description = description
        self.city = city
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.price = price
        self.age = age

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "location": self.location,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "price": self.price,
            "age": self.age,
        }


def add_data_to_mongodb(festivals):
    # Connection to MongoDB
    client = MongoClient('mongodb://root:example@localhost:27017/')
    db = client.festival_database
    collection = db.festivals

    # Inserting the data
    collection.insert_many(festivals)
    print(f"{len(festivals)} festivals inserted into MongoDB.")


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
            start_date = jsn.get("startDate")
            end_date = jsn.get("endDate")
            price = jsn.get("offers", {}).get("price")

            all_festivals.append(
                Festival(name, description, city, location, start_date, end_date, price, None).to_dict())

    add_data_to_mongodb(all_festivals)


if __name__ == "__main__":
    scrap_festival_information()
