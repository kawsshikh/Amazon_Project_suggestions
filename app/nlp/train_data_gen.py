import json
import random
import logging
from pathlib import Path
from typing import List, Tuple, Dict
import pandas as pd

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CSV_PATH = BASE_DIR /"data" /  "questions.csv"
OUTPUT_PATH = BASE_DIR / "data" / "data.json"

# Label mapping
base_map = {
    'q': 'QUERY',
    'r': 'RANK',
    's': 'STAR',
    'p': 'SPON',
    'o': 'O'
}

sponsored_patterns: List[Tuple[List[str], List[str]]] = [
    (["sponsored"], ["B-SPONSORED"]),
    (["promoted"], ["B-SPONSORED"]),
    (["not", "sponsored"], ["B-SPONSORED", "I-SPONSORED"]),
    (["not", "promoted"], ["B-SPONSORED", "I-SPONSORED"]),
    (["no", "ads"], ["B-SPONSORED", "I-SPONSORED"]),
    (["paid", "promotion"], ["B-SPONSORED", "I-SPONSORED"]),
    (["advertised"], ["B-SPONSORED"]),
    (["brand", "promotion"], ["B-SPONSORED", "I-SPONSORED"]),
    (["in", "collaboration"], ["B-SPONSORED", "I-SPONSORED"]),
    (["in", "partnership"], ["B-SPONSORED", "I-SPONSORED"]),
    (["sponsored", "content"], ["B-SPONSORED", "I-SPONSORED"]),
    (["this", "is", "an", "ad"], ["B-SPONSORED", "I-SPONSORED", "I-SPONSORED", "I-SPONSORED"]),
    (["not", "an", "ad"], ["B-SPONSORED", "I-SPONSORED", "I-SPONSORED"]),
    (["endorsement"], ["B-SPONSORED"]),
    (["in", "association", "with"], ["B-SPONSORED", "I-SPONSORED", "I-SPONSORED"]),
]


def is_transition_point(labels: List[str], i: int) -> bool:
    if i == 0 or i == len(labels):
        return True
    prev_label = labels[i - 1]
    curr_label = labels[i]
    return (prev_label.startswith("I-") and (curr_label.startswith("B-") or curr_label == "O")) or \
        (prev_label == "O" and curr_label.startswith("B-"))


def get_transition_indices(labels: List[str]) -> List[int]:
    return [i for i in range(len(labels) + 1) if is_transition_point(labels, i)]


def process_row(question: str, code: str) -> Tuple[Dict[str, List[str]], bool]:
    tokens = question.strip().split()
    input_label = code.strip() if pd.notna(code) else ""
    label_tokens = input_label.split()

    mapped_labels = []
    prev_type = None
    valid = True

    for i, token_code in enumerate(label_tokens):
        token_code = token_code.lower()
        if token_code == 'o':
            mapped_labels.append("O")
            prev_type = None
        elif token_code in base_map:
            ent_type = base_map[token_code]
            label_prefix = "B-" if prev_type != ent_type else "I-"
            mapped_labels.append(f"{label_prefix}{ent_type}")
            prev_type = ent_type
        else:
            logger.warning(f"Invalid label: '{token_code}' at position {i + 1} in question: {question}")
            valid = False
            break

    if len(mapped_labels) != len(tokens):
        logger.warning(
            f"Token/label mismatch: {len(tokens)} tokens vs {len(mapped_labels)} labels\nQuestion: {question}")
        valid = False

    return ({"tokens": tokens, "labels": mapped_labels}, valid)


def insert_sponsor_phrases(data: List[Dict[str, List[str]]]) -> None:
    for item in data:
        tokens = item["tokens"]
        labels = item["labels"]

        insert_tokens, insert_labels = random.choice(sponsored_patterns)
        valid_indices = get_transition_indices(labels)
        insert_index = random.choice(valid_indices) if valid_indices else 0

        item["tokens"] = tokens[:insert_index] + insert_tokens + tokens[insert_index:]
        item["labels"] = labels[:insert_index] + insert_labels + labels[insert_index:]


def main():
    questions_df = pd.read_csv(CSV_PATH)
    data = []
    invalid_entries = []

    for question, code in zip(questions_df['question'], questions_df['code']):
        entry, valid = process_row(question, code)
        if valid:
            data.append(entry)
        else:
            invalid_entries.append({"question": question, "code": code})

    insert_sponsor_phrases(data)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

    logger.info("✅ Sponsor phrases inserted safely with no BIO violations.")

    if invalid_entries:
        logger.warning("\n--- Invalid Entries ---")
        for entry in invalid_entries:
            logger.warning(entry["question"])


if __name__ == "__main__":
    main()
