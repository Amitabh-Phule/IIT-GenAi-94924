#Exercise 3: Fetch data from JSONPlaceholder API and save to a file
import requests
import json
from datetime import datetime
import os

def fetch_posts_from_api(url="https://jsonplaceholder.typicode.com/posts"):
    try:
        print("Fetching data from JSONPlaceholder API...")
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        data = response.json()
        print(f"Successfully fetched {len(data)} posts!")
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None


def save_to_file(data, filename="posts_data.json"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"Data saved successfully to '{filename}'")
        return True
    except IOError as e:
        print(f"Error saving to file: {e}")
        return False


def main():
    print("=" * 60)
    print("JSONPlaceholder API Data Fetcher")
    print("=" * 60)
    
    # Fetch data from API
    posts_data = fetch_posts_from_api()
    
    if posts_data:
        # Create filename with timestamp
        filename = f"posts_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        # Get the current directory (Exercise03 folder)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        filepath = os.path.join(current_dir, filename)
        
        # Save to file in Exercise03 directory
        save_to_file(posts_data, filepath)
        
        # Display summary
        print("\n" + "=" * 60)
        print("Summary:")
        print(f"Total posts fetched: {len(posts_data)}")
        print(f"First post title: {posts_data[0].get('title', 'N/A')}")
        print(f"File saved as: {filepath}")
        print("=" * 60)
        
        # Display the JSON content
        print("\nJSON File Content:")
        print("-" * 60)
        print(json.dumps(posts_data, indent=4, ensure_ascii=False))
        print("-" * 60)
    else:
        print("Failed to fetch data from API.")


if __name__== "__main__":
    main()