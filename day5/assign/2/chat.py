import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# --- Configuration (Kept simple) ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GROQ_API_KEY or not GEMINI_API_KEY:
    
    raise ValueError("API keys are missing")

# Get user input
user_input = input("Ask me anything: ")
if not user_input.strip():
    print("Input cannot be empty.")
    exit()

# --- Gemini API Call ---
gemini_url = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent?key=" + GEMINI_API_KEY
)

gemini_payload = {
    "contents": [
        {
            "parts": [
                {"text": user_input}
            ]
        }
    ],
    "generationConfig": {
        "temperature": 0.7,
        "maxOutputTokens": 1024
    }
}

gemini_response = requests.post(
    gemini_url,
    headers={"Content-Type": "application/json"},
    json=gemini_payload,
    timeout=30 
)

# --- Groq API Call ---
groq_url = "https://api.groq.com/openai/v1/chat/completions"

groq_headers = {
    "Authorization": f"Bearer {GROQ_API_KEY}",
    "Content-Type": "application/json"
}

groq_payload = {
    "model": "llama-3.3-70b-versatile",
    "messages": [
        {"role": "user", "content": user_input}
    ]
}

groq_response = requests.post(
    groq_url,
    headers=groq_headers,
    json=groq_payload,
    timeout=30
)




# Gemini Output
if gemini_response.status_code == 200:
   
    try:
        gemini_text = gemini_response.json()["candidates"][0]["content"]["parts"][0]["text"]
        print("Gemini Bot:", gemini_text)
    except (KeyError, IndexError, ValueError):
        print("Gemini Error: Successful call, but failed to parse response content.")
else:
    print("Gemini Error:", gemini_response.text)

# Groq Output
if groq_response.status_code == 200:
    
    try:
        groq_text = groq_response.json()["choices"][0]["message"]["content"]
        print("Groq Bot:", groq_text)
    except (KeyError, IndexError, ValueError):
        print("Groq Error: Successful call, but failed to parse response content.")
else:
    print("Groq Error:", groq_response.text)