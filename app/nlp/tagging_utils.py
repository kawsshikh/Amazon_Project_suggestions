from typing import Dict, Any
from transformers import BertTokenizerFast
from app.models.config import label2id


tokenizer = BertTokenizerFast.from_pretrained("bert-base-uncased")   #tokenization


def tokenize_and_align_labels(example):
    tokenized = tokenizer(
        example["tokens"],
        is_split_into_words=True,
        truncation=True,
        padding='max_length',
        max_length=32
    )   ## output: input_ids, attention_mask, token_type_ids, labels

    word_ids = tokenized.word_ids()  ##tokenised word_ids
    labels = []
    previous_word_idx = None

    for word_idx in word_ids:           ##re-assigning the labels to the word_ids
        if word_idx is None:
            labels.append(-100)  # special tokens
        elif word_idx != previous_word_idx:
            labels.append(label2id[example["labels"][word_idx]])  # first subword
        else:
            # Subword token: use I- label (not B-)
            label = example["labels"][word_idx]
            if label.startswith("B-"):
                label = label.replace("B-", "I-")
            labels.append(label2id[label])
        previous_word_idx = word_idx

    tokenized["labels"] = labels
    return tokenized