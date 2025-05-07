import requests
from Config.config import WEATHER_API_KEY

def fetch_weather(city: str) -> dict:
    """
    Récupère les données météo brutes pour une ville donnée via WeatherAPI.com
    et renvoie uniquement les champs essentiels.
    """
    url = "https://api.weatherapi.com/v1/current.json"
    params = {
        "key": WEATHER_API_KEY,  # votre clé depuis https://www.weatherapi.com/my/
        "q": city,
        "lang": "fr"
    }

    # Appel à l'API
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    # Extraction des informations utiles
    loc     = data.get("location", {})
    cur     = data.get("current", {})
    return {
        "city":        loc.get("name"),
        "temp":        cur.get("temp_c"),
        "description": cur.get("condition", {}).get("text"),
        "humidity":    cur.get("humidity"),
        "wind_speed":  cur.get("wind_kph"),
    }
