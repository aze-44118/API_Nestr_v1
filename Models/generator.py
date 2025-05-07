from Fetchers.calendar import fetch_calendar
from Fetchers.weather import fetch_weather
from Fetchers.news import fetch_news
from Supabase.user_data import load_user_environment



def generation_data(user_id):

    # summary_text = f"{user_id} – « Sans cesse la politesse exige, la bienséance ordonne ; sans cesse on suit des usages, jamais son propre génie. »\n"

    
    
    # Partie ci dessous supprime pour les tests
    
    # 1. Récupération des données utilisateur depuis Supabase
    user_env = load_user_environment(user_id)
    if not user_env:
        return "Erreur : impossible de récupérer les préférences utilisateur."
    
    # 1.1. Creer les variables de ces donnees (ToBeDone)
    city = city = user_env.get("default_city", "lieu inconnu")
    calendar_urls = [
    user_env.get("calendar_url_1"),
    user_env.get("calendar_url_2"),
    user_env.get("calendar_url_3"),
    ]

    # on enlève les None ou chaînes vides
    calendar_urls = [url for url in calendar_urls if url]

    # 2. Récupération des scripts via les builders
    user_data = user_env.get("first_name", "Donovan")
    agenda_data = fetch_calendar(calendar_urls)
    weather_data = fetch_weather(city)   
    news_data = fetch_news()  # On peut ajouter le nombre d'article demande

    # 4. Préparation du message brut
    summary_data = ""
    summary_data += (
        f"\nInfos Utilisateur\n{user_data}\n\n"
        f"\nMétéo\n{weather_data}\n\n"
        f"Agenda\n{agenda_data}\n\n"
        f"Actu\n{news_data}\n\n"
    )
    

    return summary_data


