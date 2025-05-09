import os
import json
import datetime
from google.cloud import texttospeech
from google.oauth2 import service_account

# ① Charge directement le JSON depuis l'env var
gcp_json = os.environ.get("GCP_SA_JSON")
if not gcp_json:
    raise RuntimeError("GCP_SA_JSON missing")

# ② Crée les credentials et le client UNE SEULE FOIS
info  = json.loads(gcp_json)
creds = service_account.Credentials.from_service_account_info(info)
client = texttospeech.TextToSpeechClient(credentials=creds)

def generate_audio_from_text_google(
    podcast_text: str,
    user_id: str,
    voice_name: str = "fr-FR-Wavenet-A"
) -> str:
    synthesis_input = texttospeech.SynthesisInput(text=podcast_text)
    voice = texttospeech.VoiceSelectionParams(
        language_code=voice_name.split("-")[0],  # "fr-FR" ou "en-US"
        name=voice_name
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.10,
        pitch=2.0,
        volume_gain_db=2.0,
        effects_profile_id=["headphone-class-device"]
    )
    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    output_path = f"/tmp/{user_id}_{ts}_podcast.mp3"
    with open(output_path, "wb") as out:
        out.write(response.audio_content)
    return output_path
