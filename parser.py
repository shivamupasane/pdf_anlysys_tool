import re
SPEAKER_PREFIXES = [
    "Mr.",
    "1Ir.",   # OCR mistake for Mr.
    "Shri",
    "Shrimati",
    "Smt.",
    "Dr.",
    "Pandit",
    "Maulana",
    "Nawab",
    "Sir",
    "The Honourable",
    "The Honorable",
    "Mr. Speaker",
    "Mr. President",
]

def find_debate_start(text):
    lines = text.split("\n")

    for i, line in enumerate(lines):
        line_upper = line.upper()

        if "ASSEMBLY MET" in line_upper:
            return i

    return None
def is_valid_speaker(name):
    if len(name) < 5:
        return False
    if name in ["CONTENTS", "VOLUME", "MONDAY"]:
        return False
    return True

def is_speaker_line(line):
    line = line.strip()

    if ":" not in line:
        return False

    before = line.split(":", 1)[0].strip()

    # reject colon inside constituency: (Madras: General)
    if "(" in before and ")" not in before:
        return False

    if len(before) < 5 or len(before) > 130:
        return False

    reject_words = [
        "DECLARATION",
        "ELECTION",
        "QUESTION",
        "BILL",
        "STATEMENT",
        "MEMBERS MADE",
        "FOLLOWING MEMBERS",
        "PROPOSER",
        "SECONDER",
        "PAGE",
        "VOLUME",
        "SESSION",
    ]

    if any(w in before.upper() for w in reject_words):
        return False

    speaker_patterns = [
        r"^Mr\. President",
        r"^Mr\. Speaker",
        r"^Mr\. ",
        r"^Shri ",
        r"^Shrimati ",
        r"^Smt\. ",
        r"^Dr\. ",
        r"^Sir ",
        r"^Pandit ",
        r"^Nawab ",
        r"^Maulana ",
        r"^The Honourable ",
        r"^The Honorable ",
        r"^The HOnourable ",
        r"^The llonourable ",
    ]

    return any(re.match(p, before) for p in speaker_patterns)
def extract_speaker(line):
    return line.split(":", 1)[0].strip()
def find_first_real_speaker(lines):
    import re

    for i, line in enumerate(lines):
        if ":" in line:
            name = line.split(":")[0].strip()

            # must look like a real name (not "Bill", not "Monday")
            if re.match(r'^[A-Z .\-]+$', name) and len(name.split()) >= 2:
                return i

    return 0
def trim_to_debate(text):
    marker = "ELECTION OF THE SPEAKER."
    index = text.find(marker)

    if index != -1:
        return text[index:]

    marker = "The Assembly met"
    index = text.find(marker)

    if index != -1:
        return text[index:]

    return text

def split_into_speeches(text):
    pattern = r'((Mr\.|Shri|Dr\.|Sir|Pandit|Shrimati|Nawab)[^:]{0,100}:)'

    parts = re.split(pattern, text)

    speeches = []
    current_speaker = None

    i = 0
    while i < len(parts):
        part = parts[i]

        if part and part.endswith(":"):
            current_speaker = part[:-1].strip()
            speech_text = ""

            if i + 3 < len(parts):
                speech_text = parts[i + 3]

            speeches.append({
                "speaker_raw": current_speaker,
                "speech": speech_text.strip()
            })

            i += 4
        else:
            i += 1

    return speeches
def is_valid_speaker(name):
    if len(name) < 5:
        return False

    if name.lower().startswith("the following"):
        return False

    return True
def normalize_speaker(name):
    name = name.strip()

    # 1. Remove bracket content (roles, constituency)
    name = re.sub(r'\(.*?\)', '', name)

    # 2. Remove common prefixes
    prefixes = [
        "The Honourable",
        "The Honorable",
        "Honourable",
        "Honorable",
        "Shri",
        "Shrimati",
        "Smt.",
        "Mr.",
        "Dr.",
        "Sir",
        "Pandit",
        "Maulana",
        "Nawab"
    ]

    for p in prefixes:
        name = re.sub(rf'\b{p}\b\.?', '', name)

    # 3. Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()

    # 4. Handle special roles
    if "Speaker" in name:
        return "Speaker"

    if "President" in name:
        return "President"

    return name
def is_valid_entry(s):
    speaker = s["speaker_raw"].strip()
    speech = s["speech"].strip()

    if len(speaker) < 5:
        return False

    if len(speech) < 20:
        return False

    bad_speakers = ["Sir, I move", "General)", "Mr."]
    if speaker in bad_speakers:
        return False

    return True
def is_valid_speech(s):
    if len(s["speaker_raw"]) < 5:
        return False
    if len(s["speech"]) < 20:
        return False
    return True


def normalize_text(text):
    replacements = {
        "1Ir.": "Mr.",
        "lIr.": "Mr.",
        "Ilr.": "Mr.",
        "Kr. Speaker": "Mr. Speaker",
        "Mr. !lpeaker": "Mr. Speaker",
        "Mr. Spaaker": "Mr. Speaker",
        "Mr. Sp6aker": "Mr. Speaker",
        "Mr. Spea.ker": "Mr. Speaker",
        "Mr. Spr": "Mr. Speaker",
        "Mr. Sprakf.'!'": "Mr. Speaker",
        "Jawabarlal Nebr1i": "Jawaharlal Nehru",
        "Jawaharlal .ahru": "Jawaharlal Nehru",
        "AssemblI": "Assembly",
        "ConBtituent": "Constituent",
        "legis lative": "legislative",
        "Honour able": "Honourable",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = re.sub(r"[ \t]+", " ", text)
    return text