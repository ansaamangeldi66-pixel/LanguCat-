import speech_recognition as sr
from gtts import gTTS
import os
import asyncio
from pydub import AudioSegment
import aiofiles
from utils.audio_converter import convert_ogg_to_wav

class SpeechHandler:
    def __init__(self):
        self.recognizer = sr.Recognizer()

    async def convert_speech_to_text(self, voice_file_path: str) -> str:
        """Convert voice message to text asynchronously"""
        try:
            # Convert OGG to WAV
            wav_path = await convert_ogg_to_wav(voice_file_path)
            
            # Use threading to run speech recognition asynchronously
            loop = asyncio.get_event_loop()
            text = await loop.run_in_executor(None, self._recognize_speech, wav_path)
            
            # Check if text was successfully recognized
            if not text or len(text.strip()) == 0:
                raise Exception("Could not detect any speech in the audio")
            
            # Cleanup
            os.remove(wav_path)
            os.remove(voice_file_path)
            
            return text.strip()
        except Exception as e:
            raise Exception(f"Speech recognition error: {str(e)}")

    def _recognize_speech(self, audio_path: str) -> str:
        """Internal method to perform speech recognition"""
        with sr.AudioFile(audio_path) as source:
            audio = self.recognizer.record(source)
            try:
                return self.recognizer.recognize_google(audio)
            except sr.UnknownValueError:
                raise Exception("Speech could not be understood")
            except sr.RequestError:
                raise Exception("Could not request results from speech recognition service")

    async def convert_text_to_speech(self, text: str, output_path: str) -> str:
        """Convert text to speech asynchronously"""
        try:
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self._generate_speech, text, output_path)
            return output_path
        except Exception as e:
            raise Exception(f"Text-to-speech error: {str(e)}")

    def _generate_speech(self, text: str, output_path: str):
        """Internal method to generate speech"""
        tts = gTTS(text=text, lang='en')
        tts.save(output_path)
