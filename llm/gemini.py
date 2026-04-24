import os
import requests
from dotenv import load_dotenv

# 🔹 Load environment variables
load_dotenv()

API_KEY = os.getenv("OPENROUTER_API_KEY")


# 🔹 Common function to call LLM safely
def call_llm(prompt):
    """
    Sends request to OpenRouter LLM and returns response text.
    Includes error handling and validation.
    """
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "http://localhost",
            "X-Title": "GenAI Scraper"
        }

        data = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {
                    "role": "user",
                    "content": prompt.strip()
                }
            ],
            "temperature": 0
        }

        response = requests.post(url, headers=headers, json=data, timeout=20)
        result = response.json()

        # 🔹 Validate response
        if "choices" in result:
            content = result["choices"][0]["message"]["content"]
            return clean_json_response(content)

        elif "error" in result:
            return f"Error: {result['error']}"

        else:
            return f"Unexpected response: {result}"

    except Exception as e:
        return f"Error: {str(e)}"


# 🔹 STEP 1: Extract fields from user input
def extract_fields(user_input):
    """
    Converts user input string into JSON list of fields.
    Example: "title, price" → ["title", "price"]
    """

    prompt = f"""
    Convert the following into a clean JSON list of field names.

    Input: {user_input}

    Return STRICT JSON only.
    No markdown.
    No explanation.

    Example:
    Input: product name, price
    Output: ["product name", "price"]
    """

    return call_llm(prompt)


# 🔹 STEP 2: Extract data from HTML using AI
def extract_with_ai(html, fields):
    """
    Uses LLM to extract structured data from HTML.
    Only used when rule-based extraction fails.
    """

    try:
        # 🔹 Clean HTML (avoid JSON breaking)
        cleaned_html = html.replace("\n", " ").replace('"', "'")

        # 🔹 Limit size for performance
        cleaned_html = cleaned_html[:3000]

        prompt = f"""
        You are a data extraction AI.

        Extract the following fields:
        {fields}

        Rules:
        - Return ONLY JSON list
        - No markdown
        - No explanation
        - If data not found, return null

        HTML:
        {cleaned_html}
        """

        return call_llm(prompt)

    except Exception as e:
        return f"Error: {str(e)}"


# 🔹 Helper: Clean JSON response
def clean_json_response(response):
    """
    Removes markdown formatting like ```json ... ```
    Ensures valid JSON string output.
    """

    try:
        if not isinstance(response, str):
            return response

        # Remove markdown blocks
        if "```" in response:
            parts = response.split("```")
            for part in parts:
                if "{" in part or "[" in part:
                    response = part.strip()
                    break

        # Remove "json" word if present
        response = response.replace("json", "").strip()

        return response

    except Exception:
        return response