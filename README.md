* Amazon Product Suggestion System using BERT-based Named Entity Recognition and FastAPI

This project uses a fine-tuned BERT NER model and a FastAPI interface to:

- 📝 Collect free-form product queries through an interactive HTML form (via FastAPI GET method).

- 🔍 Extract structured product intent — including product name, minimum rating, number of suggestions, and sponsorship preference — from natural language input using the NER model.

- 🛒 Scrape Amazon listings using Playwright based on the extracted intent.

- 🧠 Rank and filter results using custom heuristics to highlight relevant products.

- 📤 Display results via FastAPI POST method, returning curated product recommendations.
