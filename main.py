import json
from utils import parse_speeches, clean_text, extract_text_from_pdf
from parser import is_speaker_line, find_debate_start, is_valid_speaker, trim_to_debate, normalize_text,normalize_speaker,is_valid_speech
INPUT_FILE = "data/input/cald_01_17-11-1947.pdf"
OUTPUT_FILE = "data/output/output.json"

def main():

    text = extract_text_from_pdf(INPUT_FILE)
    text = normalize_text(text)
    text = trim_to_debate(text)   # 🔥 VERY IMPORTANT

    speeches = parse_speeches(text)
    speeches = [s for s in speeches if is_valid_speaker(s["speaker_raw"])]
    speeches = [s for s in speeches if is_valid_speech(s)]
    unique_speakers = set([s["speaker_raw"] for s in speeches])

    print("Total speeches:", len(speeches))
    print("Unique speakers:", len(unique_speakers))
    merged = []
    # Clean
    for s in speeches:
        s["speaker"] = normalize_speaker(s["speaker_raw"])
        s["speech"] = clean_text(s["speech"])
        s["date"] = "1947-11-17"
        s["session"] = "Constituent Assembly"
        s["source"] = "cad_volume_1"
    merged = []
    for s in speeches:
        if merged and merged[-1]["speaker"] == s["speaker"]:
            merged[-1]["speech"] += " " + s["speech"]
        else:
            merged.append(s)

    speeches = merged      

    # Save
    with open(OUTPUT_FILE, "w") as f:
        json.dump(speeches, f, indent=2)

    print(f"Saved {len(speeches)} speeches")


if __name__ == "__main__":
    main()