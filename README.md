# GenAI Web Scraper

## Overview

This project is a GenAI-powered web scraper that extracts structured data dynamically from any website.
It combines traditional scraping techniques with LLM-based extraction and a modular agent-based architecture.

---

##  Features

* Dynamic field extraction using LLM
* Supports multiple websites
* Hybrid scraping (Requests + Selenium)
* Structured JSON output
* Streamlit UI for user interaction
* FastAPI backend for processing
* CSV download support

---

##  Architecture


Streamlit UI
     ↓
FastAPI Backend
     ↓
Orchestrator (Agents)
     ↓
Scraper (Requests + Selenium)
     ↓
BeautifulSoup (Data Cleaning)
     ↓
LLM (Optional Extraction)
     ↓
Structured Output


---

##  Setup Instructions

### 1️ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 2️ Run Backend

```bash
uvicorn main:app --reload
```

---

### 3️ Run Frontend

```bash
streamlit run app.py
```

---

##  Usage

1. Enter a website URL
2. Enter fields (comma-separated, e.g., `title, price`)
3. Click Scrape Data
4. View extracted results
5. Download CSV if needed

---

##  Tech Stack

* FastAPI (Backend)
* Streamlit (Frontend)
* BeautifulSoup (Parsing)
* Selenium (Dynamic scraping)
* OpenRouter / LLM (AI extraction)

---

## Limitations

* Some websites block scraping
* Dynamic websites may require Selenium
* LLM responses may vary

---

##  Future Improvements

* Pagination support
* Multi-website comparison
* Database storage
* Advanced UI (React)

---

## Author

Aadhya Reddy
