import os

# Telegram Bot Token
TELEGRAM_TOKEN = os.environ['TELEGRAM_TOKEN']
# HuggingFace API
HUGGINGFACE_API_TOKEN = os.environ['HUGGINGFACE_API_TOKEN']
HUGGINGFACE_API_URL = "https://api-inference.huggingface.co/models/facebook/blenderbot-400M-distill"

# Speech Recognition
TEMP_VOICE_PATH = "temp_voice"
TEMP_AUDIO_PATH = "temp_audio"

# Create temporary directories if they don't exist
os.makedirs(TEMP_VOICE_PATH, exist_ok=True)
os.makedirs(TEMP_AUDIO_PATH, exist_ok=True)

# Supported Commands
COMMANDS = {
    'start': 'Start the conversation',
    'help': 'Show available commands',
    'reset': 'Reset the conversation'
}
