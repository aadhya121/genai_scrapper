import requests

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        return response.text
    except Exception as e:
        return f"Error fetching HTML: {str(e)}"