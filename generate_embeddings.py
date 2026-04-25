from pymongo import MongoClient
from sentence_transformers import SentenceTransformer

client = MongoClient("mongodb://localhost:27017")
db = client["parliament_ai"]
speeches_col = db["speeches"]

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
# all-MiniLM-L6-v2 is fast and good for general semantic search. It outputs 384-dim vectors.

def main():
    cursor = speeches_col.find(
        {"embedding": {"$exists": False}},
        {"speech": 1}
    )

    count = 0

    for doc in cursor:
        speech = doc.get("speech", "")
        if not speech.strip():
            continue

        embedding = model.encode(speech).tolist()

        speeches_col.update_one(
            {"_id": doc["_id"]},
            {"$set": {"embedding": embedding}}
        )

        count += 1
        print(f"Embedded: {count}")

    print("Embedding generation completed.")


if __name__ == "__main__":
    main()