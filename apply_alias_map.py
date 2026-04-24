import json
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "parliament_ai"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

speeches_col = db["speeches"]


def apply_alias_map():
    with open("alias_map.json", "r", encoding="utf-8") as f:
        alias_map = json.load(f)

    total_updated = 0

    for alias, canonical in alias_map.items():
        if alias == canonical:
            continue
        result = speeches_col.update_many(
            {"speaker": alias},
            {"$set": {"speaker": canonical}}
        )

        total_updated += result.modified_count

        print(f"{alias} -> {canonical}: {result.modified_count} updated")

    print(f"Total updated: {total_updated}")


if __name__ == "__main__":
    apply_alias_map()