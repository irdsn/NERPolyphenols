"""
Script to perform a stratified split of JSON documents by query into train/val/test folders.
"""

import json
import random
from collections import defaultdict
from shutil import copy2
from utils.paths import RAW_DATA_DIR, TRAIN_DIR, VAL_DIR, TEST_DIR, DOCS_DIR

# Reproducibility
random.seed(42)

LOG_PATH = DOCS_DIR / "split_log.txt"

# Ensure output directories exist
for path in [TRAIN_DIR, VAL_DIR, TEST_DIR]:
    path.mkdir(parents=True, exist_ok=True)

# Group documents by query
query_buckets = defaultdict(list)

for filepath in RAW_DATA_DIR.glob("*.json"):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            doc = json.load(f)
        query = doc.get("query", "").strip()
        if query:
            query_buckets[query].append(filepath)
    except Exception as e:
        print(f"[WARNING] Skipping file {filepath.name}: {e}")

# Stratified split per query
log_lines = []
total_docs = 0
global_train, global_val, global_test = 0, 0, 0

for query, files in sorted(query_buckets.items()):
    total_docs += len(files)
    n = len(files)

    n_train = int(n * 0.65)
    remaining = n - n_train
    n_val = int(remaining * 20 / 35)
    n_test = remaining - n_val

    shuffled = files[:]
    random.shuffle(shuffled)

    train = shuffled[:n_train]
    val = shuffled[n_train:n_train + n_val]
    test = shuffled[n_train + n_val:]

    global_train += len(train)
    global_val += len(val)
    global_test += len(test)

    for f in train:
        copy2(f, TRAIN_DIR / f.name)
    for f in val:
        copy2(f, VAL_DIR / f.name)
    for f in test:
        copy2(f, TEST_DIR / f.name)

    log_lines.append(f"Query: {query}")
    log_lines.append(f"  Total: {len(files)}")
    log_lines.append(f"  Train: {len(train)}")
    log_lines.append(f"  Val:   {len(val)}")
    log_lines.append(f"  Test:  {len(test)}\n")

# Save split log
LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(LOG_PATH, "w", encoding="utf-8") as log_file:
    log_file.write(f"Total documents: {total_docs}\n")
    log_file.write(f"Saved to:\n  Train: {TRAIN_DIR} ({global_train} files)\n")
    log_file.write(f"  Val:   {VAL_DIR} ({global_val} files)\n")
    log_file.write(f"  Test:  {TEST_DIR} ({global_test} files)\n")
    log_file.write(f"  >>> Total after split: {global_train + global_val + global_test}\n\n")
    log_file.write("Details by query:\n\n")
    log_file.write("\n".join(log_lines))

print("[INFO] Stratified split completed successfully.")
