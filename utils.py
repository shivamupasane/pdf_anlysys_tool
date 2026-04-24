import pdfplumber
from datetime import datetime
import re
from parser import is_speaker_line
def extract_text_from_pdf(file_path):
    full_text = []

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text = page.extract_text()
            if text:
                full_text.append(text)

    return "\n".join(full_text)
def extract_speaker(line):
    return line.split(":")[0].strip()
def extract_date_from_filename(filename):
    # match dd-mm-yyyy
    match = re.search(r'(\d{2})-(\d{2})-(\d{4})', filename)

    if match:
        day, month, year = match.groups()
        return f"{year}-{month}-{day}"  # ISO format

    return None
def parse_speeches(text):
    speeches = []
    current_speaker = None
    buffer = []

    for line in text.split("\n"):
        line = line.strip()

        if not line:
            continue

        if is_speaker_line(line):
            if current_speaker and buffer:
                speeches.append({
                    "speaker_raw": current_speaker,
                    "speech": " ".join(buffer)
                })

            current_speaker = extract_speaker(line)
            buffer = [line.split(":", 1)[1].strip()]

        else:
            if current_speaker:
                buffer.append(line)

    if current_speaker and buffer:
        speeches.append({
            "speaker_raw": current_speaker,
            "speech": " ".join(buffer)
        })

    return speeches
def clean_text(text):
    text = re.sub(r"\s+", " ", text)

    # remove page markers
    text = re.sub(r"\(\s*\d+\s*\)", " ", text)
    text = re.sub(r"\d+\s+CONSTITUENT ASSEMBLY.*?\]", " ", text)

    # remove repeated spaces again
    text = re.sub(r"\s+", " ", text)

    return text.strip()