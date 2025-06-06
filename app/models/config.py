import json
import logging
from pathlib import Path

#logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#label
label_list = [
    "O",  # unimportant POS,
    "B-QUERY", "I-QUERY",  # Product to search
    "B-RANK", "I-RANK",  # Number of Results
    "B-SPONSORED", "I-SPONSORED",  # sponsored
    "B-STAR", "I-STAR"]  # rating of the product

#     labels for future expansion
#     "B-PRICE", "I-PRICE",
#     "B-BRAND", "I-BRAND",
#     "B-COLOR", "I-COLOR",
#     "B-CATEGORY", "I-CATEGORY",
#     "B-FEATURE", "I-FEATURE",
#     "B-CONDITION", "I-CONDITION"
# ]

#mappings
label2id = {label: i for i, label in enumerate(label_list)}   #numeric representation
id2label = {i: label for label, i in label2id.items()}          # numeric to label mapping

#relative path
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CORRECTIONS_FILE = BASE_DIR / "data" / "data.json"


train_data = []
if CORRECTIONS_FILE.is_file():
    try:
        with open(CORRECTIONS_FILE) as f:
            train_data = json.load(f)
    except json.JSONDecodeError:
        logger.warning("file exists but contains invalid JSON.")
else:
    logger.warning(f"Corrections file not found at {CORRECTIONS_FILE}")
