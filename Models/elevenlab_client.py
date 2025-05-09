import os
import requests
from Config import ELEVENLAB_API_KEY  # charge dynamiquement via ta edge function


ELEVENLAB_VOICE_ID = os.environ.get("ELEVENLAB_VOICE_ID", "EXAVITQu4vr4xnSDxMaL")  # Voix par défaut

def generate_audio_from_text_elevenlab(text: str, user_id: str, voice_id: str = None) -> str:
    try:
        if not ELEVENLAB_API_KEY:
            raise ValueError("❌ API Key ElevenLabs manquante.")
        
        selected_voice_id = voice_id or ELEVENLAB_VOICE_ID
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}"

        headers = {
            "xi-api-key": ELEVENLAB_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,
            "model_id": "eleven_multilingual_v2",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            print(f"❌ Erreur ElevenLabs (TTS): {response.status_code} - {response.text}")
            return None

        output_path = f"static/{user_id}_tts_eleven.mp3"
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        with open(output_path, "wb") as f:
            f.write(response.content)

        print(f"✅ Audio ElevenLabs sauvegardé dans {output_path}")
        return output_path

    except Exception as e:
        print(f"❌ Exception dans generate_audio_from_text_elevenlab: {e}")
        return None

