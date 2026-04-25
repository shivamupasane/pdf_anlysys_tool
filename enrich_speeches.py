# enrich_speeches.py

from pymongo import MongoClient
import re

client = MongoClient("mongodb://localhost:27017")
db = client["parliament_ai"]
speeches_col = db["speeches"]


def detect_speech_type(text):
    t = text.lower()

    if "i beg to move" in t or "i move" in t:
        return "motion_or_bill"
    if "question" in t:
        return "question"
    if "i oppose" in t:
        return "opposition"
    if "i support" in t:
        return "support"
    return "debate"


def extract_keywords(text):
    keywords = []

    topic_words = [
        "constitution", "railway", "finance", "labour", "health",
        "refugees", "bill", "assembly", "budget", "industry",
        "education", "law", "foreign", "workers"
    ]

    lower = text.lower()

    for word in topic_words:
        if word in lower:
            keywords.append(word)

    return keywords


def main():
    for doc in speeches_col.find({}):
        speech = doc.get("speech", "")

        word_count = len(re.findall(r"\w+", speech))
        speech_type = detect_speech_type(speech)
        keywords = extract_keywords(speech)

        speeches_col.update_one(
            {"_id": doc["_id"]},
            {
                "$set": {
                    "word_count": word_count,
                    "speech_type": speech_type,
                    "keywords": keywords
                }
            }
        )

    print("Speech enrichment completed.")


if __name__ == "__main__":
    main()