import json
import re
from pymongo import MongoClient
from rapidfuzz import fuzz

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "parliament_ai"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

speakers_col = db["speakers"]

OUTPUT_FILE = "alias_map_generated.json"


def normalize_for_matching(name):
    name = name.lower()

    # remove roles/constituency
    name = re.sub(r"\(.*?\)", "", name)

    # remove common titles
    titles = [
        "the honourable",
        "honourable",
        "the honorable",
        "honorable",
        "shri",
        "shrimati",
        "smt",
        "mr",
        "dr",
        "sir",
        "pandit",
        "maulana",
        "nawab",
        "minister for law",
        "minister for labour",
        "minister for finance",
    ]

    for t in titles:
        name = re.sub(rf"\b{re.escape(t)}\b", "", name)

    # remove punctuation and OCR noise
    name = re.sub(r"[^a-z\s]", " ", name)
    name = re.sub(r"\s+", " ", name).strip()

    return name


def choose_canonical(name1, name2):
    # Prefer cleaner/shorter name
    n1 = normalize_for_matching(name1)
    n2 = normalize_for_matching(name2)

    if len(n1) <= len(n2):
        return name1
    return name2


def main():
    speakers = list(speakers_col.find({}, {"_id": 0, "speaker": 1, "speech_count": 1}))

    names = [s["speaker"] for s in speakers if s.get("speaker")]
    alias_map = {}

    for i, name1 in enumerate(names):
        norm1 = normalize_for_matching(name1)

        if len(norm1) < 4:
            continue

        for name2 in names[i + 1:]:
            norm2 = normalize_for_matching(name2)

            if len(norm2) < 4:
                continue

            score = fuzz.token_sort_ratio(norm1, norm2)

            if score >= 88:
                canonical = choose_canonical(name1, name2)

                if name1 != canonical:
                    alias_map[name1] = canonical

                if name2 != canonical:
                    alias_map[name2] = canonical

                print(f"{score} | {name1}  -->  {canonical}")
                print(f"{score} | {name2}  -->  {canonical}")
                print("-" * 80)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(alias_map, f, indent=2, ensure_ascii=False)

    print(f"\nGenerated {len(alias_map)} alias mappings")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    main()