from fastapi import FastAPI
from pydantic import BaseModel
import json

# ✅ Only use orchestrator
from agents.orchestrator import run_pipeline
from llm.gemini import extract_fields

app = FastAPI()

# 📥 Request schema
class ScrapeRequest(BaseModel):
    url: str
    fields: str


@app.get("/")
def home():
    return {"message": "GenAI Web Scraper Running 🚀"}


@app.post("/scrape")
def scrape(data: ScrapeRequest):

    # 🧠 STEP 1: Extract fields using LLM
    raw_output = extract_fields(data.fields)

    # 🧹 STEP 2: Normalize fields
    try:
        parsed_fields = json.loads(raw_output)

        if isinstance(parsed_fields, list) and len(parsed_fields) > 0:
            if isinstance(parsed_fields[0], dict):
                parsed_fields = list(parsed_fields[0].keys())

    except Exception:
        parsed_fields = [data.fields]

    # 🤖 STEP 3: Run full agent pipeline
    final_data = run_pipeline(data.url, parsed_fields)

    # 📤 FINAL RESPONSE
    return {
        "url": data.url,
        "fields": parsed_fields,
        "data": final_data
    }