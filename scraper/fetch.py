import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup


def fetch_html(url):
    """
    Fetch HTML content from a website using requests first,
    and fallback to Selenium for dynamic content.
    Also performs basic cleaning to reduce noise.
    """

    try:
        # 🔹 STEP 1: Try using requests (fast)
        response = requests.get(url, timeout=10)

        if response.status_code != 200:
            return f"Error: Failed to fetch page (status code {response.status_code})"

        html = response.text

        # If content is too small → likely dynamic site
        if len(html) < 500:
            html = fetch_with_selenium(url)

        # 🔹 STEP 2: Clean HTML using BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")

        # 🔹 STEP 3: Try extracting product sections (common pattern)
        products = soup.find_all("article", class_="product_pod")

        if products:
            # Return only relevant section (cleaner for processing)
            return str(products)

        # 🔹 STEP 4: Fallback → return full cleaned HTML
        return str(soup)

    except Exception as e:
        return f"Error fetching HTML: {str(e)}"


def fetch_with_selenium(url):
    """
    Fallback method for dynamic websites using Selenium.
    """

    try:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome(options=options)
        driver.get(url)

        html = driver.page_source
        driver.quit()

        return html

    except Exception as e:
        return f"Error with Selenium: {str(e)}"