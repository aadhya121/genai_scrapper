from agents.planner import plan
from agents.scraper_agent import scrape
from agents.extractor_agent import extract
from agents.postprocess_agent import clean

def run_pipeline(url, fields):
    plan_data = plan(fields)

    html = scrape(url)

    raw_data = extract(html, plan_data["fields"])

    final_data = clean(raw_data)

    return final_data