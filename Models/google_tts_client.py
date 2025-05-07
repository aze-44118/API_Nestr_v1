import os
import datetime
from google.cloud import texttospeech

# Définit l’environnement pour Google Cloud
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Config/google_credentials.json"

def generate_audio_from_text_google(podcast_text: str, user_id: str, voice_name: str = "fr-FR-Wavenet-A") -> str:
    """
    Génére un MP3 à partir de texte via Google WaveNet.
    :param podcast_text: contenu à convertir
    :param user_id: identifiant utilisateur (pour nommage fichier)
    :param voice_name: nom précis de la voix Google (ex: fr-FR-Wavenet-A)
    :return: chemin local du fichier MP3 généré
    """
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=podcast_text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name=voice_name
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3,
        speaking_rate=1.05,
        pitch=3.0,
        volume_gain_db=2.0,
        effects_profile_id=["small-bluetooth-speaker-class-device"]
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