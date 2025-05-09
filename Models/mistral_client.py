# Services/mistral_service.py

from mistralai import Mistral
from Config.config import MISTRAL_API_KEY, ASSISTANT_COURRIEL, AGENT_SCRIPT, AGENT_MOOD

# Initialize the Mistral client using the same env-var you were
# using for OPENAI_API_KEY (now holding your Mistral key).
client = Mistral(api_key=MISTRAL_API_KEY)  # hDbiL2BXqzFUMiJ51M7zHWdQmR93ONXP

def nestr_briefing_courriel(user_message: str) -> str | None:
    """
    Send the user's prompt to your 'nestr_breifing_courriel' agent
    and return its reply.
    """
    try:
        response = client.agents.complete(
            agent_id=ASSISTANT_COURRIEL,              # e.g. "ag:4a0364e7:20250429:untitled-agent:008907fc"
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Mistral Error: {e}")
        return None

def nestr_briefing_script(user_message: str) -> str | None:
    """
    Send the user's prompt to your 'nestr_briefing_script' agent
    and return its reply.
    """
    try:
        response = client.agents.complete(
            agent_id=AGENT_SCRIPT,  # ← autre agent Mistral
            messages=[{"role": "user", "content": user_message}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"❌ Mistral Error (script): {e}")
        return None

def nestr_daily_mood(user_message: str) -> dict | None:
    from json import loads
    try:
        resp = client.agents.complete(
            agent_id=AGENT_MOOD,
            messages=[{"role": "user", "content": user_message}],
        )
        raw = resp.choices[0].message.content or ""
        print("🔍 RAW MOOD RESPONSE:", repr(raw))   # <— ajoute ce log
        # Si le modèle embed des backticks, on les enlève :
        if raw.startswith("```"):
            # enlève ```json  ``` éventuels
            raw = raw.strip("```").replace("json", "").strip()
        return loads(raw)
    except Exception as e:
        print(f"❌ Mistral Error (mood): {e}")
        return None

