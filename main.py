from fastapi import FastAPI
from pydantic import BaseModel
import json

#  Imports
from agents.orchestrator import run_pipeline
from llm.gemini import extract_fields

app = FastAPI()


#  Request schema
class ScrapeRequest(BaseModel):
    url: str
    fields: str


#  Home route (health check)
@app.get("/")
def home():
    return {"message": "GenAI Web Scraper Running 🚀"}


#  Main scraping API
@app.post("/scrape")
def scrape(data: ScrapeRequest):

    #  STEP 0: Validate input
    if not data.url or not data.fields:
        return {"error": "URL and fields are required"}

    if not data.url.startswith("http"):
        return {"error": "Invalid URL format. Must start with http/https"}

    #  STEP 1: Extract fields using LLM
    try:
        raw_output = extract_fields(data.fields)
    except Exception as e:
        return {"error": f"Field extraction failed: {str(e)}"}

    #  STEP 2: Normalize fields (string → list)
    try:
        parsed_fields = json.loads(raw_output)

        # Handle inconsistent LLM output
        if isinstance(parsed_fields, list) and len(parsed_fields) > 0:
            if isinstance(parsed_fields[0], dict):
                parsed_fields = list(parsed_fields[0].keys())

    except Exception:
        # fallback if LLM fails
        parsed_fields = [data.fields]

    #  STEP 3: Run pipeline (scraper + extraction)
    try:
        final_data = run_pipeline(data.url, parsed_fields)
    except Exception as e:
        return {"error": f"Pipeline failed: {str(e)}"}

    #  STEP 4: Validate output
    if not final_data:
        return {"error": "No data extracted from the website"}

    #  FINAL RESPONSE
    return {
        "url": data.url,
        "fields": parsed_fields,
        "data": final_data
    }