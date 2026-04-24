from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["parliament_ai"]

speaker = "Jagjivan Ram"

results = db.speeches.find(
    {"speaker": speaker},
    {"_id": 0, "speaker": 1, "date": 1, "speech": 1}
)

for r in results:
    print(r["speaker"], r["date"])
    print(r["speech"][:300])
    print("-" * 80)