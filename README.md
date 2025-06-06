# 🛍️ Amazon Product Intent Extractor

This project leverages a **fine-tuned BERT NER model** and a **FastAPI** backend to create an intelligent product query system. It converts free-form user input into structured queries, scrapes Amazon using **Playwright**, and returns ranked product suggestions in an interactive HTML interface.

---

## 🚀 Features

- 📝 **Natural Language Input Form**  
  Interactive HTML form using FastAPI (`GET`) to collect user queries like:  
  _"Show me 5 noise-canceling headphones rated above 4.3 that are not sponsored."_

- 🤖 **Named Entity Recognition (NER)**  
  Extracts structured product intent from the query using a fine-tuned **BERT model**, including:
  - Product name  
  - Minimum rating  
  - Number of results requested  
  - Sponsorship preference

- 🌐 **Amazon Scraping with Playwright**  
  Automates browsing and extracts live product listings from Amazon.

- 🧠 **Smart Ranking & Filtering**  
  Uses heuristics to sort and prioritize relevant products (e.g., rating, sponsored status, reviews).
---

## 📁 Project Structure
```text
project_root/
├── app/
│ ├── models/ # Configs and ID mappings
│ │ └── config.py
│ ├── nlp/ # Core logic for training and tagging
│ │ ├── train_model.py
│ │ ├── train_data_gen.py
│ │ ├── tagging_utils.py
│ │ └── model_trainer_config.py
│ ├── services/ # JSON generation, scraping, reinforcement
│ │ ├── JSON_query_gen.py
│ │ ├── reinforce.py
│ │ ├── table_format.py
│ │ └── web_scrape.py
│ ├── utils/ # UI generation and HTML helpers
│ │ └── html_text.py
│ └── main.py # FastAPI app entry point
│
├── data/ # Input datasets
│ ├── data.json
│ └── questions.csv
│
├── ner-model/ # Trained BERT model directory
├── result.json # Final product listing results
├── requirements.txt # Project dependencies
├── README.md # Project documentation
├── run.py # FastAPI Uvicorn runner
└── first_run.py # One-time model trainer
```
---



- 📤 **FastAPI Response with Results**  
  Returns filtered product listings via FastAPI `POST`, rendering them on a results HTML page.

---
## 🛠️ Installation Rules for Amazon Product Intent Extractor

Follow these steps to set up the project on your local machine:

1. Clone the Repository


git clone https://github.com/kawsshikh/Amazon_Project_suggestions.git
cd Amazon_Project_suggestions

2. Set Up a Virtual Environment


Create and activate a virtual environment:

- On Windows:
  python -m venv .venv
  .venv\Scripts\activate

- On macOS/Linux:
  python3 -m venv .venv
  source .venv/bin/activate

3. Install Required Packages


pip install -r requirements.txt

4. Install Playwright and Its Dependencies


python -m playwright install

(This installs the necessary browser binaries for scraping.)

5. (Optional) Train the BERT NER Model


python -m first_run

(Skip if you already have a trained model saved in `./ner-model`.)

6. Run the FastAPI Application


python -m run

Then open your browser and go to: http://localhost:8002
