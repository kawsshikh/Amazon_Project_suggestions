from typing import List, Optional, Callable, Dict, Any
from transformers import Trainer, TrainingArguments, BertTokenizerFast, BertForTokenClassification, EarlyStoppingCallback
from datasets import Dataset
from app.models.config import label_list, id2label, label2id
from app.nlp.tagging_utils import tokenize_and_align_labels
from seqeval.metrics import accuracy_score, f1_score


def model_fn(model_name_or_path :str ="bert-base-uncased"):
    return BertForTokenClassification.from_pretrained(
        model_name_or_path,
        num_labels=len(label_list),
        id2label=id2label,
        label2id=label2id
    )


def training_args(batch_size: int =4, epochs: int =5, logging_steps: int =10):
    return TrainingArguments(
        output_dir="./bert-ner-output",
        per_device_train_batch_size=batch_size,
        per_device_eval_batch_size=batch_size,
        num_train_epochs=epochs,
        logging_steps=logging_steps,
        logging_dir="./logs",
        save_strategy="epoch",
        evaluation_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1",
        save_total_limit=1,
    )


def default_metrics(p: Any) -> Dict[str, float]:
    predictions, labels = p
    predictions = predictions.argmax(axis=-1)

    true_labels = [[id2label[l] for l in label if l != -100] for label in labels]
    true_preds = [[id2label[pred] for (pred, lab) in zip(pred_row, label_row) if lab != -100]
                  for pred_row, label_row in zip(predictions, labels)]

    return {
        "accuracy": accuracy_score(true_labels, true_preds),
        "f1": f1_score(true_labels, true_preds)
    }


def trainer_fn(model_name_path: str ="bert-base-uncased", data=[], test_data=[],
               batch_size: int =4, epochs: int =5, logging_steps: int =10, compute_metrics: Optional[Callable] =None):

    tokenizer = BertTokenizerFast.from_pretrained(model_name_path)
    train_dataset = Dataset.from_list(data).shuffle(seed=42).map(tokenize_and_align_labels)
    test_dataset = Dataset.from_list(test_data).map(tokenize_and_align_labels)

    return Trainer(
        model=model_fn(model_name_path),
        args=training_args(batch_size, epochs, logging_steps),
        train_dataset=train_dataset,
        eval_dataset=test_dataset,
        tokenizer=tokenizer,
        compute_metrics = compute_metrics or default_metrics,
        callbacks = [EarlyStoppingCallback(early_stopping_patience=2)]
        )

