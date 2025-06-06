import json
from transformers import BertTokenizerFast, BertForTokenClassification
import torch
from app.services.JSON_query_gen import extract_data
from app.models.config import  id2label, train_data, CORRECTIONS_FILE
import sys
import subprocess
# from web_scrape import process_request



model_path = "./ner-model"
tokenizer = BertTokenizerFast.from_pretrained(model_path)
model = BertForTokenClassification.from_pretrained(model_path)

count =0


try:
    with open(CORRECTIONS_FILE, "r") as f:
        corrected_examples = json.load(f)
except FileNotFoundError:
    corrected_examples = []



def predict_labels(tokens):
    encoding = tokenizer(tokens, is_split_into_words=True, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**encoding)
    predictions = torch.argmax(outputs.logits, dim=-1)[0].tolist()
    word_ids = encoding.word_ids(batch_index=0)
    label_predictions = []
    for idx, word_id in enumerate(word_ids):
        if word_id is None:
            continue
        if idx == 0 or word_id != word_ids[idx - 1]:
            label_predictions.append(id2label[predictions[idx]])
    return label_predictions


def correct_labels(tokens):
    corrected = []
    print("Reference to input numbers")
    print(id2label)
    print("question")
    print(tokens)
    while True:
        input_str = input("Enter label numbers separated by space: ")
        try:
            input_numbers = [id2label[num] for num in list(map(int, input_str.split()))]

            for tok, pred in zip(tokens, input_numbers):
                print(f"{tok:>10} → {pred} ")
            flag_correct = input("are the parameters right?")
            if flag_correct.lower() == "y":
                return input_numbers
        except Exception as e:
            print(f"Error: {e}")
            continue

def main():
    global count
    developer_flag = input(">> Are you a developer?y/n").strip().lower() == "y"
    if developer_flag:
        print("thank you for being a developer! With you help, I will re-train model after every 5 mistakes")

    print("Type 'exit' to quit. Input your sentence tokenized (e.g., find me top 10 laptop):\n")

    while True:
        sentence = input(">> ").strip()
        if sentence.lower() == "exit":
            break

        tokens = sentence.split()
        predicted = predict_labels(tokens)
        print(predicted)
        print(tokens)
        json_query = extract_data(tokens, predicted)
        # process_request(json_query)
        print(json_query)
        if developer_flag:
            print("\nPredicted Labels:")
            for tok, label in zip(tokens, predicted):
                print(f"{tok:>10} → {label}")
            flag_json = input("Are the metrics correct? y/n").strip()
            if flag_json.lower() == "y":
                continue
            else:
                predicted = correct_labels(tokens)
                corrected_examples.append({
                    "tokens": tokens,
                    "predicted": predicted
                })
                count = count+1
                if count >= 5:
                    with open(CORRECTIONS_FILE, "w") as file:
                        json.dump(corrected_examples, file, indent=2)
                    print("OOPS!! 5 mistakes done \n retraining model")
                    subprocess.run([sys.executable, "train_model.py"])
                    print("Model re-trained successfully.\n")
                    count = 0






if __name__ == "__main__":
    main()
