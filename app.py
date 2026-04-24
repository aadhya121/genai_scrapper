import streamlit as st
import requests
import pandas as pd

# Page config
st.set_page_config(page_title="GenAI Web Scraper", layout="centered")

st.title("🤖 GenAI Web Scraper")
st.write("Enter a website URL and fields to extract data")

# Inputs
url = st.text_input(" Enter Website URL", "https://books.toscrape.com")
fields = st.text_input(" Enter Fields (comma separated)", "title, price")

# Button
if st.button(" Scrape Data"):

    if not url or not fields:
        st.warning("Please enter both URL and fields")
    else:
        with st.spinner("Extracting data..."):

            try:
                #  Call backend API
                response = requests.post(
                    "http://127.0.0.1:8000/scrape",
                    json={"url": url, "fields": fields}
                )

                result = response.json()

                st.success(" Extraction Complete")

                #  DEBUG (very important)
                st.subheader(" Raw API Response")
                st.write(result)

                #  Fields
                st.subheader(" Extracted Fields")
                st.write(result.get("fields"))

                #  Data
                st.subheader(" Extracted Data")
                data = result.get("data")

                #  Handle list (correct case)
                if isinstance(data, list):
                    st.json(data)

                    #  BONUS: CSV Download
                    df = pd.DataFrame(data)
                    st.download_button(
                        "⬇️ Download CSV",
                        df.to_csv(index=False),
                        "scraped_data.csv"
                    )

                #  Handle string / error case
                else:
                    st.warning("Data is not in expected format")
                    st.write(data)

            except Exception as e:
                st.error(f" Error: {str(e)}")