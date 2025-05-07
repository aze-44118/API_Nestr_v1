# Supabase/supabase_client.py

"""
Centralise la création et l'accès au client Supabase en mode service-role.
"""

from dotenv import load_dotenv
import os
from supabase import create_client as _create_client

# Charge les variables d'environnement depuis .env
load_dotenv()

# URL de votre projet Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")

SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
if not SUPABASE_URL or not SUPABASE_SERVICE_ROLE_KEY:
    raise RuntimeError("Missing SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY")

# Clé service-role (contourne RLS pour le back-end)
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# Vérifie que tout est bien configuré
if not SUPABASE_URL:
    raise RuntimeError("Environment variable SUPABASE_URL is not set!")
if not SUPABASE_ANON_KEY:
    raise RuntimeError("Environment variable SUPABASE_ANON_KEY is not set!")

# Initialise une instance partagée du client Supabase en service-role
supabase = _create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def get_connection():
    """
    Retourne l'instance partagée du client Supabase (service-role).
    À utiliser partout où on a besoin d'un accès back-end complet.
    """
    return supabase

def create_client(url: str = SUPABASE_URL, key: str = SUPABASE_ANON_KEY):
    """
    Crée et renvoie une nouvelle instance du client Supabase.
    Utile si vous devez instancier un client avec une autre clé
    (par exemple l'anon-key pour des appels front-end).
    :param url: URL du projet Supabase
    :param key: Clé d'accès (service-role ou anon)
    """
    return _create_client(url, key)

def get_client():
    return _create_client(SUPABASE_URL, SUPABASE_ANON_KEY)

