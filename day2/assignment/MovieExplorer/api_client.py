import requests
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Correctly read API key
api_key = os.getenv("OMDB_API_KEY")

if not api_key:
    raise ValueError(
        "❌ ERROR: OMDB_API_KEY not found. Create a .env with OMDB_API_KEY=your_key"
    )

BASE_URL = "http://www.omdbapi.com/"

def search_movies(query, limit=5):
    response = requests.get(
        BASE_URL,
        params={"s": query, "apikey": api_key, "type": "movie"}
    )
    response.raise_for_status()
    data = response.json()

    movies = []
    if data.get("Response") == "True":
        for item in data["Search"][:limit]:
            imdb_id = item["imdbID"]
            details = requests.get(
                BASE_URL,
                params={"i": imdb_id, "apikey": api_key}
            ).json()
            movies.append(details)

    return movies
