import os
import datetime
from typing import List, Dict
from pydub import AudioSegment
from Models.google_tts_client import generate_audio_from_text_google

# Mapping des voix par speaker
VOICE_PROFILES = {
    "Présentateur": "fr-FR-Wavenet-B",
    "Diane": "fr-FR-Wavenet-A",
    "Etienne": "fr-FR-Wavenet-D",
    "Marc": "fr-FR-Wavenet-C",
}

INTRO_PATH = "Static/intro.mp3"
OUTRO_PATH = "Static/outro.mp3"
TEMP_DIR = "/tmp"

def generate_multivoice_podcast(script: List[Dict[str, str]], user_id: str) -> str:
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

        # Appel du TTS avec voix personnalisée
        segment_path = generate_audio_from_text_google(
            podcast_text=text,
            user_id=f"{user_id}_{i}",
            voice_name=voice_name
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
