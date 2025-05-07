import os
import openai
import datetime

def generate_audio_from_text(podcast_text: str, user_id: str) -> str:
    """
    Génère un fichier MP3 à partir de podcast_text via l'API OpenAI TTS.
    :param podcast_text: Le texte du podcast à transformer en audio.
    :param user_id: Identifiant utilisateur, utilisé pour nommer le fichier.
    :return: Chemin du fichier MP3 généré.
    """
    # Configurez votre clé API OpenAI (depuis une variable d'environnement)
    OPENAI_API_KEY="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"
    openai.api_key = OPENAI_API_KEY
    
    # Appel à l'API Text-to-Speech
    audio_response = openai.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=podcast_text,
    )
    
    # Récupère les octets audio
    audio_bytes = audio_response.read()     

    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d_%H-%M-%S')
    
    # Prépare le chemin de sortie
    output_path = f"/tmp/{user_id}_{ts}_podcast.mp3"
    
    # Écrit le fichier MP3
    with open(output_path, "wb") as f:
        f.write(audio_bytes)
    
    return output_path
