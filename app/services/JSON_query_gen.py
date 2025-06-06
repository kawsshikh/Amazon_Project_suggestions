from transformers import pipeline
from number_parser import parser
import re
import random
from typing import List, Dict

# Load model once
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

def sponsor_detection(text: str) -> bool:
    if not text.strip():
        return True
    labels = ["sponsored allowed", "sponsored not allowed"]
    result = classifier(text, candidate_labels=labels)
    return result["labels"][0] == "sponsored allowed"

def text_to_number(raw_text: str) -> float:
    if not raw_text.strip():
        return 0.0
    parsed_text = parser.parse(raw_text)
    match = re.search(r"\d+(?:\.\d+)?", parsed_text)
    return float(match.group()) if match else 0.0

def process_limit(text):
    if text_to_number(text) > 0:
        return int(text_to_number(text))
    limit_labels = ["few", "many", "couple"]
    result = classifier(text, candidate_labels=limit_labels)
    if result["labels"][0] == "few":
        return random.randint(3,5)
    elif result["labels"][0] == "many":
        return random.randint(8,10)
    else:
        return random.randint(3,10)

def format_query(tokens):
    clean_tokens = [re.sub(r'^\W+|\W+$', '', token) for token in tokens]
    clean_tokens = [token for token in clean_tokens if token]
    return " ".join(clean_tokens).strip()

def extract_data(tokens: list[str], labels: list[str]) -> dict:
    fields = {
        "query": [],
        "limit": [],
        "stars": [],
        "sponsored": []
    }

    label_map = {
        "QUERY": "query",
        "RANK": "limit",
        "SPONSORED": "sponsored",
        "STAR": "stars"
    }

    for tok, label in zip(tokens, labels):
        for key in label_map:
            if label.endswith(key):
                fields[label_map[key]].append(tok)
                break

    query_metrics = {
        "query": format_query(fields["query"]),
        "limit": int(process_limit(" ".join(fields["limit"]))) if fields["limit"] else random.randint(3,10),
        "stars": text_to_number(" ".join(fields["stars"])) if fields["stars"] else 4,
        "sponsored": sponsor_detection(" ".join(fields["sponsored"]))
    }

    return query_metrics
