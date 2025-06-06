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
🛠️ Installation Instructions for Amazon Product Intent Extractor

Follow these steps to set up the project on your local machine:


🔹 **Clone the Repository**
```bash
git clone https://github.com/kawsshikh/Amazon_Project_suggestions.git
cd Amazon_Project_suggestions
```



🔹 **Set Up a Virtual Environment**

- **On Windows:**
```bash
python -m venv .venv
.venv\Scripts\activate
```

- **On macOS/Linux:**
```bash
python3 -m venv .venv
source .venv/bin/activate
```



🔹 **Install Required Packages**
```bash
pip install -r requirements.txt
```



🔹 **Install Playwright and Its Dependencies**
```bash
python -m playwright install
```

> This installs the necessary browser binaries for scraping.



🔹 **(Optional) Train the BERT NER Model**
```bash
python -m first_run
```

> Skip if you already have a trained model saved in `./ner-model`.



🔹 **Run the FastAPI Application**
```bash
python -m run
```

Then open your browser and go to:  
🌐 [http://localhost:8002](http://localhost:8002)

---
### 📡 API Endpoints

| Method | Endpoint       | Description                    |
|--------|----------------|--------------------------------|
| GET    | `/`            | Renders the input query form   |
| POST   | `/result`      | Accepts query input, returns filtered product cards |

---

## 🧠 How It Works
```markdown


1. User Input (Free-Form Text):
   - You enter a natural query like:
     _"Find me 5 green tea powders rated above 4 stars and not sponsored"_

2. **NER Model Extraction:**
   - The BERT-based NER model extracts:
     - query: `green tea powder`
     - stars: `4`
     - limit: `5`
     - sponsored: False    

3. **Playwright Scraper:**
   - Scrapes Amazon for real product listings using headless browsing.

4. **Heuristics Engine:**
   - filters and sorts the data according to the user's preference

5. **Result Display:**
   - FastAPI renders the HTML with product name, rating, reviews, price, etc.
```
---
## 📽 Demo
🔹 **Query obtained as Input from FastAPI GET**
  - list non sponsored seven Harry Potter lego sets with at least 4.5 star rating.

🔹 **ETL - NER**
 - detects "Harry Potter lego set" as query
 - detects seven as number of suggestions -> converts str to int
 - rating as 4.5
 - sponsor is flagged false
 - constructs a JSON


🔹 **Web Scraping using Plawright**
- Gathers the query
- transforms into a search URL
- transforms the HTML content to DataFrame
- apply filter and sort


 🔹 **Output sent through FastAPI POST**
- Gathered output is passed to users via FastAPI Post


![Demo](demo.gif)

---
### ⚠️ Note on Web Scraping

- This tool is for **educational purposes**.
- Web scraping Amazon may trigger anti-bot mechanisms.
- Use headless = `False` if Amazon blocks headless mode.

---
### 🧰 Tech Stack

- 🐍 Python 3.10+
- 🤖 Transformers (`BERT`, HuggingFace)
- 🌐 FastAPI
- 🎭 Playwright
- 📊 Pandas, LXML
- 🧪 Uvicorn (for local dev server)

## 📜 License

This project is licensed under the [MIT License](LICENSE).
