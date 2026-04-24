from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["parliament_ai"]

db.speeches.create_index("speaker")
db.speeches.create_index("date")
db.speeches.create_index("source_file")
db.speeches.create_index([("speech", "text")])

print("Indexes created")