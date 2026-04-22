import streamlit as st
import requests

st.set_page_config(page_title="GenAI Web Scraper", layout="centered")

st.title("🤖 GenAI Web Scraper")
st.write("Enter a website URL and fields to extract data")

# Inputs
url = st.text_input("🌐 Enter Website URL")
fields = st.text_input("🧠 Enter Fields (comma separated)", "product name, price")

# Button
if st.button("🚀 Scrape Data"):

    if not url or not fields:
        st.warning("Please enter both URL and fields")
    else:
        with st.spinner("Extracting data..."):

            try:
                response = requests.post(
                    "http://127.0.0.1:8000/scrape",
                    json={"url": url, "fields": fields}
                )

                result = response.json()

                st.success("✅ Extraction Complete")

                st.subheader("📌 Extracted Fields")
                st.write(result["fields"])

                st.subheader("📊 Extracted Data")
                st.json(result["data"])

            except Exception as e:
                st.error(f"Error: {str(e)}")