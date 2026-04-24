import os
import json
from utils import extract_text_from_pdf, clean_text, parse_speeches, extract_date_from_filename
from parser import (
    trim_to_debate,
    normalize_speaker,
    is_valid_entry,
    normalize_text
)

INPUT_DIR = "data/input"
OUTPUT_FILE = "data/output/output.json"


def main():
    all_speeches = []

    for filename in os.listdir(INPUT_DIR):
        if not filename.lower().endswith(".pdf"):
            continue

        file_path = os.path.join(INPUT_DIR, filename)
        print(f"Processing: {filename}")

        text = extract_text_from_pdf(file_path)
        text = normalize_text(text)
        text = trim_to_debate(text)

        speeches = parse_speeches(text)
        file_date = extract_date_from_filename(filename)
        for s in speeches:
            s["speech"] = clean_text(s["speech"])
            s["speaker"] = normalize_speaker(s["speaker_raw"])

            # metadata
            s["source_file"] = filename
            s["session"] = "Constituent Assembly"
            s["date"] = file_date   # 🔥 USE HERE

        speeches = [s for s in speeches if is_valid_entry(s)]

        print(f"  speeches found: {len(speeches)}")
        all_speeches.extend(speeches)

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_speeches, f, indent=2, ensure_ascii=False)

    print("===================================")
    print(f"Total speeches saved: {len(all_speeches)}")
    print(f"Unique speakers: {len(set(s['speaker'] for s in all_speeches))}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()