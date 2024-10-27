from openai import AsyncOpenAI

from keys import api_key

client = AsyncOpenAI(api_key=api_key)

async def stt(file_path):
    with open(file_path, "rb") as audio_file:
        transcription = await client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
        )
    return transcription.text