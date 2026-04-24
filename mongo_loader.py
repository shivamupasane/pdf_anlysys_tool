import json
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "parliament_ai"
COLLECTION_NAME = "speeches"

INPUT_FILE = "data/output/output.json"


def load_to_mongodb():
    client = MongoClient(MONGO_URI)
    db = client[DB_NAME]
    speeches_collection = db[COLLECTION_NAME]

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        speeches = json.load(f)

    if not speeches:
        print("No speeches found.")
        return

    speeches_collection.delete_many({})
    speeches_collection.insert_many(speeches)

    print(f"Inserted {len(speeches)} speeches into MongoDB")


if __name__ == "__main__":
    load_to_mongodb()