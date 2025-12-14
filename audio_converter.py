import os
from pydub import AudioSegment
import asyncio
from config import TEMP_AUDIO_PATH

async def convert_ogg_to_wav(ogg_path: str) -> str:
    """Convert OGG file to WAV format asynchronously"""
    try:
        wav_path = os.path.join(TEMP_AUDIO_PATH, f"{os.path.splitext(os.path.basename(ogg_path))[0]}.wav")
        
        # Run conversion in thread pool
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, _convert_audio, ogg_path, wav_path)
        
        return wav_path
    except Exception as e:
        raise Exception(f"Audio conversion error: {str(e)}")

def _convert_audio(input_path: str, output_path: str):
    """Internal function to convert audio files"""
    audio = AudioSegment.from_ogg(input_path)
    audio.export(output_path, format="wav")
