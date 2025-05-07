# Supabase/user_data.py

from .supabase_client import get_connection  # client service-role
import uuid

def load_user_environment(user_id: str) -> dict | None:
    """
    Charge les informations utilisateur depuis la table `user_env`.
    Renvoie un dictionnaire ou None si l'utilisateur n'existe pas ou en cas d'erreur.
    """
    client = get_connection()
    try:
        resp = (
            client
            .from_("user_env")                # table en minuscules
            .select("*")
            .eq("user_id", str(uuid.UUID(user_id)))
            .maybe_single()
            .execute()
        )
        # si pas de réponse ou requête échouée, retourne None
        if not resp or (hasattr(resp, "error") and resp.error):
            return None

        return resp.data or None

    except Exception:
        return None
