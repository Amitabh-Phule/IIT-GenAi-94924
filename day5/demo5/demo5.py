import os
import requests
import json
from dotenv import load_dotenv

# LOAD .env FILE
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError("GROQ_API_KEY not found. Check your .env file.")

url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

user_prompt = input("Ask anything: ")

req_data = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": user_prompt}
    ]
}

response = requests.post(url, headers=headers, json=req_data)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2))
