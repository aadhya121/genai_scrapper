from bs4 import BeautifulSoup

def extract_data(html, fields):
    try:
        soup = BeautifulSoup(html, "html.parser")

        data = []

        # 🔥 Simple demo logic (we'll improve later)
        items = soup.find_all("p")

        for item in items[:5]:  # limit output
            entry = {}

            text = item.get_text()

            for field in fields:
                entry[field] = text  # placeholder mapping

            data.append(entry)

        return data

    except Exception as e:
        return f"Error extracting data: {str(e)}"