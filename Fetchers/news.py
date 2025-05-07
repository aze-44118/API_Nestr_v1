import requests
from Config.config import NEWS_API_KEY

def fetch_news(country: str = "fr", max_articles: int = 5) -> list[dict]:
    """
    Récupère via l'API GNews les top-headlines pour un pays donné
    et renvoie la liste brute des articles (JSON minimal).
    """
    url = "https://gnews.io/api/v4/top-headlines"
    params = {
        "token":       NEWS_API_KEY,
        "lang":        "fr",
        "country":     country,
        "max":         max_articles
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    return resp.json().get("articles", [])
