import os
import requests
from dotenv import load_dotenv

# 1) Charge le .env en local
load_dotenv()

# 2) URL de l’edge + clé anon
SUPABASE_EDGE_URL      = os.getenv("SUPABASE_EDGE_URL")
SUPABASE_ANON_KEY      = os.getenv("SUPABASE_ANON_KEY")

# 3) URL REST Supabase + service role key
SUPABASE_URL           = os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")

# 4) Check rapide
for name, val in [
    ("SUPABASE_EDGE_URL", SUPABASE_EDGE_URL),
    ("SUPABASE_ANON_KEY", SUPABASE_ANON_KEY),
    ("SUPABASE_URL", SUPABASE_URL),
    ("SUPABASE_SERVICE_ROLE_KEY", SUPABASE_SERVICE_ROLE_KEY),
]:
    if not val:
        raise RuntimeError(f"Env var '{name}' missing")

# 5) Récupère TOUS les secrets depuis l’edge function
headers = {
    "Authorization": f"Bearer {SUPABASE_ANON_KEY}"
}
resp = requests.get(
    SUPABASE_EDGE_URL,
    headers=headers  # ✅ ici on passe bien l’Authorization dans les headers HTTP
)

resp.raise_for_status()
secrets = resp.json()

# 6) Expose en config
WEATHER_API_KEY      = secrets["WEATHER_API_KEY"]
NEWS_API_KEY         = secrets["NEWS_API_KEY"]
BREVO_API_KEY        = secrets["BREVO_API_KEY"]
ELEVENLAB_API_KEY    = secrets["ELEVENLAB_API_KEY"]
MISTRAL_API_KEY      = secrets["MISTRAL_API_KEY"]
ASSISTANT_COURRIEL   = secrets["ASSISTANT_COURRIEL"]
AGENT_SCRIPT         = secrets["AGENT_SCRIPT"]
AGENT_MOOD           = secrets["AGENT_MOOD"]

# 7) GCP : on récupère la JSON complète du service account
GCP_SA_JSON = secrets.get("GCP_SA_JSON")
if not GCP_SA_JSON:
    raise RuntimeError("GCP_SA_JSON missing in secrets")

# 8) Supabase Database URL
DATABASE_URL = secrets["DATABASE_URL"]

# (tu peux aussi exposer STATIC_FOLDER ou d’autres si besoin)
