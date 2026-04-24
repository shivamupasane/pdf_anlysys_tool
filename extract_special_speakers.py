import json
import re
from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "parliament_ai"
OUTPUT_FILE = "special_speakers.json"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

speakers_col = db["speakers"]


def has_special_char(name):
    # allow letters, space, dot
    return bool(re.search(r"[^a-zA-Z ]", name))


def main():
    special_map = {}

    speakers = speakers_col.find({}, {"_id": 0, "speaker": 1})

    for s in speakers:
        name = s.get("speaker", "").strip()

        if not name:
            continue

        if has_special_char(name):
            special_map[name] = ""

    # sort for readability
    special_map = dict(sorted(special_map.items()))

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(special_map, f, indent=2, ensure_ascii=False)

    print(f"Found {len(special_map)} speakers with special characters")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()