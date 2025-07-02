"""
Script: entities_extractor.py
Location: entities/
Goal: Process all abstracts from datasets/raw/ and generate versions with extracted entity candidates
      saved in entities/extracted/. Uses predefined lexicons (POLYPHENOL, FOOD, SYMPTOM).
"""

import os
import json
import spacy
from collections import defaultdict
from tqdm import tqdm
from defined.polyphenols import KNOWN_POLYPHENOLS
from defined.foods import KNOWN_FOODS
from defined.symptoms import KNOWN_SYMPTOMS
from utils.paths import RAW_DATA_DIR
from pathlib import Path

# === OUTPUT DIRECTORY ===
EXTRACTED_DIR = Path(__file__).resolve().parent / "extracted"
EXTRACTED_DIR.mkdir(parents=True, exist_ok=True)

print(f"[INFO] Input directory: {RAW_DATA_DIR}")
print(f"[INFO] Output directory: {EXTRACTED_DIR}")

# Load spaCy biomedical model or fallback to general English
try:
    nlp = spacy.load("en_core_web_sm")
except:
    nlp = spacy.load("en_core_sci_sm")

# === ENTITY EXTRACTION FUNCTION ===
def extract_entities(text):
    """
    Extract candidate entities from input text using predefined lexicons and noun chunks.
    Returns a dictionary with keys: POLYPHENOL, FOOD, SYMPTOM
    """
    doc = nlp(text)
    candidates = defaultdict(set)

    for chunk in doc.noun_chunks:
        span = chunk.text.lower().strip()

        if any(term in span for term in KNOWN_POLYPHENOLS):
            candidates['POLYPHENOL'].add(span)
        elif any(term in span for term in KNOWN_FOODS):
            candidates['FOOD'].add(span)
        elif any(term in span for term in KNOWN_SYMPTOMS):
            candidates['SYMPTOM'].add(span)

    return {k: sorted(list(v)) for k, v in candidates.items()}

# === MAIN PROCESSING LOOP ===
file_list = [f for f in os.listdir(RAW_DATA_DIR) if f.endswith('.json')]
print(f"[INFO] Processing {len(file_list)} documents from '{RAW_DATA_DIR.name}'...")

for fname in tqdm(file_list, desc="Extracting entities"):
    in_path = RAW_DATA_DIR / fname
    out_path = EXTRACTED_DIR / fname

    with open(in_path, 'r') as f:
        doc = json.load(f)

    text = doc.get("abstract", "")
    entities = extract_entities(text)

    doc["entities"] = entities  # Use consistent key now (not "defined")

    with open(out_path, 'w') as f:
        json.dump(doc, f, indent=2)

print(f"\n[INFO] {len(file_list)} documents processed and saved to '{EXTRACTED_DIR}'")
