import requests

# 🔹 Your FastAPI endpoint
URL = "http://127.0.0.1:8000/scrape"

#  Test case 1 (valid)
payload = {
    "url": "https://books.toscrape.com",
    "fields": "title, price"
}

print(" Testing valid request...\n")

response = requests.post(URL, json=payload)

print("Status Code:", response.status_code)
print("Response:", response.json())


# 🔹 Test case 2 (invalid URL)
payload_invalid = {
    "url": "abc",
    "fields": "title, price"
}

print("\n Testing invalid URL...\n")

response = requests.post(URL, json=payload_invalid)

print("Status Code:", response.status_code)
print("Response:", response.json())