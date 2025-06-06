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

project_root/
├── app/
│ ├── models/ # Configs and ID mappings
│ │ └── config.py
│ ├── nlp/ # Core logic for training and tagging
│ │ ├── train_model.py # Main training script
│ │ ├── train_data_gen.py # Training data generation
│ │ ├── tagging_utils.py # Tag-to-label helpers
│ │ └── model_trainer_config.py # Training args/config
│ ├── services/ # JSON generation, scraping, reinforcement
│ │ ├── JSON_query_gen.py
│ │ ├── reinforce.py
│ │ ├── table_format.py
│ │ └── web_scrape.py
│ ├── utils/ # UI generation and HTML helpers
│ │ └── html_text.py
│ └── main.py # FastAPI app entry point
│
├── data/ # External/generated data files
│ ├── data.json
│ └── questions.csv
│
├── ner-model/ # Saved BERT model (generated)
├── result.json # Final scraped product results
├── requirements.txt # Python dependencies
├── README.md # Project overview
├── run.py # FastAPI server launcher
└── first_run.py # One-time model training launcher


- 📤 **FastAPI Response with Results**  
  Returns filtered product listings via FastAPI `POST`, rendering them on a results HTML page.

---
