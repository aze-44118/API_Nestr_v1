import os
from google.cloud import texttospeech

# Assure-toi que la variable d'environnement est définie
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "Config/google_credentials.json"

def synthesize_text(text, output_filename):
    client = texttospeech.TextToSpeechClient()

    synthesis_input = texttospeech.SynthesisInput(text=text)

    voice = texttospeech.VoiceSelectionParams(
        language_code="fr-FR",
        name="fr-FR-Wavenet-D"
    )

    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    response = client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config
    )

    with open(output_filename, "wb") as out:
        out.write(response.audio_content)
    print(f"Audio content written to file {output_filename}")
