from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017"
DB_NAME = "parliament_ai"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

speeches_col = db["speeches"]
speakers_col = db["speakers"]


def word_count(text):
    if not text:
        return 0
    return len(text.split())


def build_speakers():
    speakers_col.delete_many({})

    pipeline = [
        {
            "$group": {
                "_id": "$speaker",
                "aliases": {"$addToSet": "$speaker_raw"},
                "speech_count": {"$sum": 1},
                "total_words": {
                    "$sum": {
                        "$size": {
                            "$split": ["$speech", " "]
                        }
                    }
                },
                "first_speech_date": {"$min": "$date"},
                "last_speech_date": {"$max": "$date"},
                "source_files": {"$addToSet": "$source_file"}
            }
        },
        {
            "$project": {
                "_id": 0,
                "speaker": "$_id",
                "aliases": 1,
                "speech_count": 1,
                "total_words": 1,
                "first_speech_date": 1,
                "last_speech_date": 1,
                "source_files": 1
            }
        }
    ]

    speakers = list(speeches_col.aggregate(pipeline))

    if speakers:
        speakers_col.insert_many(speakers)

    print(f"Created {len(speakers)} speaker records")


if __name__ == "__main__":
    build_speakers()