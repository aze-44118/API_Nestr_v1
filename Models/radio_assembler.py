import os
import datetime
from typing import List, Dict
from pydub import AudioSegment
from Models.google_tts_client import generate_audio_from_text_google
from Models.elevenlab_client import generate_audio_from_text_elevenlab


# Mapping des voix par speaker
VOICE_PROFILES = {
    "Walter": "en-US-Neural2-J",
    "Rebecca": "en-US-Neural2-F",
    "Melanie": "en-US-Neural2-G",
    "Alison": "en-US-Neural2-H",
}

ELEVENLAB_PROFILES = {
    "Walter": "J4Gklq1lvygedV6xCpKJ",     # Mister
    "Rebecca": "wLoW00IP5kfH8oiOBAPp",    # Grant wittman
    "William": "FmJ4FDkdrYIKzBTruTkV",    # David Hertel
    "Mélanie": "aD6riP1btT197c6dACmy",    # Rachel M
    "Alison": "xctasy8XvGp2cVO9HL9k",     # Alison
}

INTRO_PATH = "Static/intro.mp3"
OUTRO_PATH = "Static/outro.mp3"
TEMP_DIR = "/tmp"

def generate_multivoice_podcast(script: str, user_id: str, voice_name: str = "fr-FR-Wavenet-A") -> str:
    """
    Génère un podcast multi-voix avec générique depuis un script JSON.
    :param script: liste d'objets {"speaker": "...", "text": "..."}
    :param user_id: utilisé pour nommer le fichier
    :return: chemin du fichier MP3 final
    """
    audio_segments = []

    temp_files = []  # ← on stocke ici tous les chemins de fichiers MP3 générés

    # Ajouter le générique d'intro
    if os.path.exists(INTRO_PATH):
        audio_segments.append(AudioSegment.from_mp3(INTRO_PATH))

    # Génère les segments de chaque speaker
    for i, entry in enumerate(script):
        speaker = entry["speaker"]
        text = entry["text"]
        voice_name = VOICE_PROFILES.get(speaker, "fr-FR-Wavenet-B")
        print(f"🔊 Speaker: {speaker} — Voice: {voice_name}")

        '''
        # Appel du TTS avec voix personnalisée
        segment_path = generate_audio_from_text_google(
            podcast_text=text,
            user_id=f"{user_id}_{i}",
            voice_name=voice_name
        )
        '''
        voice_id = ELEVENLAB_PROFILES.get(speaker)
        segment_path = generate_audio_from_text_elevenlab(
            text=text,
            user_id=f"{user_id}_{i}",
            voice_id=voice_id
        )

        temp_files.append(segment_path)
        audio_segments.append(AudioSegment.from_mp3(segment_path))



    # Ajouter le générique de fin
    if os.path.exists(OUTRO_PATH):
        audio_segments.append(AudioSegment.from_mp3(OUTRO_PATH))

    # Assembler tous les morceaux
    final_audio = sum(audio_segments)

    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    output_path = os.path.join(TEMP_DIR, f"{user_id}_{ts}_radio.mp3")
    final_audio.export(output_path, format="mp3")

    # Nettoyage des fichiers temporaires
    for path in temp_files:
        try:
            os.remove(path)
        except Exception as e:
            print(f"❌ Erreur lors de la suppression du fichier temporaire : {path} – {e}")


    return output_path
