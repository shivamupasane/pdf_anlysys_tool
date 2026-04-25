from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

client = MongoClient("mongodb://localhost:27017")
db = client["parliament_ai"]
speeches_col = db["speeches"]

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


def search(query, top_k=5, speaker=None, date=None):
    query_embedding = model.encode(query).reshape(1, -1)
    mongo_filter = {"embedding": {"$exists": True}}

    if speaker:
        mongo_filter["speaker"] = speaker

    if date:
        mongo_filter["date"] = date

    docs = list(speeches_col.find(
        mongo_filter,
        {"speaker": 1, "date": 1, "speech": 1, "embedding": 1}
    ))

    results = []

    for doc in docs:
        emb = np.array(doc["embedding"]).reshape(1, -1)
        score = cosine_similarity(query_embedding, emb)[0][0]

        results.append({
            "speaker": doc.get("speaker"),
            "date": doc.get("date"),
            "score": float(score),
            "speech": doc.get("speech", "")[:500]
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:top_k]


if __name__ == "__main__":
    results = search(
    "labour workers employment",
    top_k=5,
    speaker="Jagjivan Ram"
)

    for r in results:
        print("=" * 80)
        print(r["speaker"], r["date"], "score:", round(r["score"], 4))
        print(r["speech"])