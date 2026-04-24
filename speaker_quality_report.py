from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "parliament_ai"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

speakers_col = db["speakers"]


def main():
    speakers = list(speakers_col.find({}, {"_id": 0}))

    print("\n=== Low speech count speakers ===")
    for s in sorted(speakers, key=lambda x: x.get("speech_count", 0)):
        if s.get("speech_count", 0) <= 2:
            print(s["speaker"], "| count:", s["speech_count"], "| aliases:", s.get("aliases", []))

    print("\n=== Suspicious speaker names ===")
    bad_tokens = ["Sir,", "General", ":", "Speaker:", "move", "Bill", "Question"]

    for s in speakers:
        name = s["speaker"]
        if any(t.lower() in name.lower() for t in bad_tokens):
            print(name, "| aliases:", s.get("aliases", []))

    print("\n=== Possible OCR issues ===")
    ocr_tokens = ["1", "!", "X", "[", "]", ";", "  "]

    for s in speakers:
        name = s["speaker"]
        if any(t in name for t in ocr_tokens):
            print(name, "| aliases:", s.get("aliases", []))


if __name__ == "__main__":
    main()