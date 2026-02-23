import os
from dotenv import load_dotenv

load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
API_TMDB_URL = os.getenv("API_TMDB_URL", None)