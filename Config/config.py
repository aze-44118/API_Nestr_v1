import os
import requests
from dotenv import load_dotenv

# 1) Charge le fichier .env en développement
load_dotenv()

# 2) URL de la function edge + clé anonyme (pour récupérer les secrets)
SUPABASE_EDGE_URL = os.getenv("SUPABASE_EDGE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# 3) Ton URL REST Supabase + service key (pour le client Python)
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# 4) Échoue immédiatement si l’une de ces variables est manquante
for name, val in [
    ("SUPABASE_EDGE_URL", SUPABASE_EDGE_URL),
    ("SUPABASE_ANON_KEY", SUPABASE_ANON_KEY),
    ("SUPABASE_URL", SUPABASE_URL),
    ("SUPABASE_KEY", SUPABASE_SERVICE_ROLE_KEY),
]:
    if not val:
        raise RuntimeError(f"Environment variable '{name}' is not set!")

# 5) Appelle l’edge function Supabase pour récupérer tes clés secrètes
try:
    headers = {
        "Authorization": f"Bearer {SUPABASE_SERVICE_ROLE_KEY}",
        "Content-Type":  "application/json",
    }
    resp = requests.get(SUPABASE_EDGE_URL, headers=headers)
    resp.raise_for_status()
    secrets = resp.json()

    # Expose tes clés pour le reste de l’app
    WEATHER_API_KEY       = secrets["WEATHER_API_KEY"]
    
    ASSISTANT_COURRIEL    = secrets["ASSISTANT_COURRIEL"]
    MISTRAL_API_KEY       = secrets["MISTRAL_API_KEY"]
    AGENT_SCRIPT          = secrets["AGENT_SCRIPT"]
    
    NEWS_API_KEY          = secrets["NEWS_API_KEY"]
    BREVO_API_KEY         = secrets["BREVO_API_KEY"]
    STATIC_FOLDER         = secrets.get("STATIC_FOLDER", "Static")
    DATABASE_URL          = secrets["DATABASE_URL"]
    GOOGLE_CREDENTIALS_PATH = secrets.get("GOOGLE_APPLICATION_CREDENTIALS_PATH", "Config/google_credentials.json")
    ELEVENLAB_API_KEY = secrets.get["ELEVENLAB_API_KEY"]




except Exception as e:
    print("❌ Error fetching secrets from Supabase edge function:", e)
    raise
