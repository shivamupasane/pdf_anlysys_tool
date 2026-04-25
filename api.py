from fastapi import FastAPI
from pymongo import MongoClient
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

app = FastAPI()

client = MongoClient("mongodb://localhost:27017")
db = client["parliament_ai"]
speeches_col = db["speeches"]
speakers_col = db["speakers"]

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


@app.get("/speakers")
def get_speakers():
    speakers = list(speakers_col.find({}, {"_id": 0}).sort("speech_count", -1))
    return speakers


@app.get("/speeches")
def get_speeches(speaker: str | None = None, date: str | None = None, limit: int = 20):
    query = {}

    if speaker:
        query["speaker"] = speaker

    if date:
        query["date"] = date

    results = list(
        speeches_col.find(
            query,
            {"_id": 0, "embedding": 0}
        ).limit(limit)
    )

    return results


@app.get("/semantic-search")
def semantic_search(q: str, speaker: str | None = None, top_k: int = 5):
    query_embedding = model.encode(q).reshape(1, -1)

    mongo_filter = {"embedding": {"$exists": True}}

    if speaker:
        mongo_filter["speaker"] = speaker

    docs = list(
        speeches_col.find(
            mongo_filter,
            {"_id": 0, "speaker": 1, "date": 1, "speech": 1, "embedding": 1}
        )
    )

    results = []

    for doc in docs:
        emb = np.array(doc["embedding"]).reshape(1, -1)
        score = cosine_similarity(query_embedding, emb)[0][0]

        results.append({
            "speaker": doc.get("speaker"),
            "date": doc.get("date"),
            "score": float(score),
            "speech": doc.get("speech", "")[:1000]
        })

    results.sort(key=lambda x: x["score"], reverse=True)

    return results[:top_k]