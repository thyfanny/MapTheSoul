import requests

from src.config.config import API_TMDB_URL, TMDB_API_KEY

def get_movie(title: str):
    """Fetch movie details from TMDB API based on the title"""
    params = {"api_key": TMDB_API_KEY, "query": title, "language": "pt-BR"}

    try:
        response = requests.get(API_TMDB_URL, params=params)
        data = response.json()

        if data["results"]:
            filme = data["results"][0]
            poster = f"https://image.tmdb.org/t/p/w500{filme['poster_path']}" if filme.get("poster_path") else None
            sinopse = filme.get("overview", "Sinopse não disponível.")
            return poster, sinopse
    except:
        pass

    return None, "Sinopse não disponível."