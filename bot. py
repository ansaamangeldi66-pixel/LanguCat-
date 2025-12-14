import asyncio
import telebot
from telebot.async_telebot import AsyncTeleBot
import os
from config import TELEGRAM_TOKEN, TEMP_VOICE_PATH, TEMP_AUDIO_PATH, COMMANDS
from services.speech_handler import SpeechHandler
from services.chat_handler import ChatHandler
import uuid

bot = AsyncTeleBot(TELEGRAM_TOKEN)
speech_handler = SpeechHandler()
chat_handler = ChatHandler()

@bot.message_handler(commands=['start'])
async def send_welcome(message):
    """Handle /start command"""
    welcome_text = (
        "👋 Welcome to the English Practice Bot!\n\n"
        "Send me voice messages in English, and I'll respond to help you practice.\n"
        "Use /help to see available commands."
    )
    await bot.reply_to(message, welcome_text)

@bot.message_handler(commands=['help'])
async def send_help(message):
    """Handle /help command"""
    help_text = "Available commands:\n"
    for command, description in COMMANDS.items():
        help_text += f"/{command} - {description}\n"
    await bot.reply_to(message, help_text)

@bot.message_handler(commands=['reset'])
async def reset_conversation(message):
    """Handle /reset command"""
    chat_handler.reset_conversation(message.from_user.id)
    await bot.reply_to(message, "Conversation has been reset!")

@bot.message_handler(content_types=['voice'])
async def handle_voice(message):
    """Handle voice messages"""
    try:
        print(f"\nProcessing voice message from user {message.from_user.id}")
        print("Step 1: Voice message received and processing started")
        # Send typing status
        await bot.send_chat_action(message.chat.id, 'typing')

        # Download voice message
        print("Step 2: Downloading voice message...")
        file_info = await bot.get_file(message.voice.file_id)
        voice_file_path = os.path.join(TEMP_VOICE_PATH, f"{uuid.uuid4()}.ogg")
        downloaded_file = await bot.download_file(file_info.file_path)
        print(f"Step 3: Voice message saved to {voice_file_path}")
        
        # Save voice message
        with open(voice_file_path, 'wb') as voice_file:
            voice_file.write(downloaded_file)

        # Convert speech to text
        text = await speech_handler.convert_speech_to_text(voice_file_path)
        await bot.reply_to(message, f"You said: {text}")

        # Get chat response
        response = await chat_handler.get_response(message.from_user.id, text)
        await bot.reply_to(message, f"Response: {response}")

        # Convert response to speech
        audio_path = os.path.join(TEMP_AUDIO_PATH, f"{uuid.uuid4()}.mp3")
        await speech_handler.convert_text_to_speech(response, audio_path)

        # Send voice response
        with open(audio_path, 'rb') as audio_file:
            await bot.send_voice(message.chat.id, audio_file)

        # Cleanup
        os.remove(audio_path)

    except Exception as e:
        error_message = "Sorry, I couldn't process your voice message. "
        if "Speech could not be understood" in str(e):
            error_message += "I couldn't understand the speech clearly. Please try speaking more clearly."
        elif "Could not detect any speech" in str(e):
            error_message += "I couldn't detect any speech in your message. Please make sure you're speaking clearly."
        elif "Could not request results" in str(e):
            error_message += "There was a problem with speech recognition. Please try again later."
        else:
            error_message += "An unexpected error occurred. Please try again."
        
        await bot.reply_to(message, error_message)

async def main():
    """Main function to run the bot"""
    try:
        print("Bot started... Waiting for messages")
        print("Available commands:", ", ".join(COMMANDS.keys()))
        await bot.polling(non_stop=True, timeout=60)
    except Exception as e:
        print(f"Bot error: {str(e)}")
        print("Restarting bot in 5 seconds...")
        await asyncio.sleep(5)
        await main()

if __name__ == "__main__":
    asyncio.run(main())
