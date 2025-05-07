import os
import datetime
from google.cloud import texttospeech

# Définit l’environnement pour Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Config/google_credentials.json"

def generate_audio_from_text_google(podcast_text: str, user_id: str) -> str:
    """
    Génére un MP3 à partir de texte via Google WaveNet.
    :return: chemin local du fichier généré
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=podcast_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name="fr-FR-Chirp-HD-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3, 
        peaking_rate=0.95,
        pitch=1.5,
        volume_gain_db=2.0,
        effects_profile_id=["telephony-class-application"]
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
