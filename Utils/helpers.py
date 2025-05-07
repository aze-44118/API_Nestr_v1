import json

def load_user_profile():
    """
    Charge les données de profil utilisateur depuis le fichier JSON.
    """
    profile_path = os.path.join(os.path.dirname(__file__), '..', 'Static', 'user_profile.json')
    try:
        with open(profile_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Erreur : fichier user_profile.json introuvable.")
        return {}

def get_calendar_urls(profile):
    return profile.get("calendar", {}).get("calendar_urls", [])

def get_news_api_key(profile):
    return profile.get("news", {}).get("news_api_key", "")

def get_location(profile):
    return profile.get("location", {})