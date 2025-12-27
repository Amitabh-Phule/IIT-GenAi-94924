from api_client import search_movies
from math_utils import average, maximum, minimum
from storage import save_json, save_csv

def main():
    query = input("Enter movie search term: ").strip()
    if not query:
        print("You must enter a search term.")
        return

    movies = search_movies(query)
    if not movies:
        print("No movies found.")
        return

    ratings = []
    results = []
    print("\nMovies Found:")
    for m in movies:
        title = m.get("Title")
        year = m.get("Year")
        imdb_rating = float(m.get("imdbRating")) if m.get("imdbRating") not in [None, "N/A"] else 0
        ratings.append(imdb_rating)
        print(f"{title} ({year}) - IMDb Rating: {imdb_rating}")
        results.append({"Title": title, "Year": year, "IMDb Rating": imdb_rating})

    print("\nStatistics:")
    print("Max IMDb Rating:", maximum(ratings))
    print("Min IMDb Rating:", minimum(ratings))
    print("Average IMDb Rating:", round(average(ratings), 2))

    save_json(results, "data/movies.json")
    save_csv(results, "data/movies.csv")

if __name__ == "__main__":
    main()
