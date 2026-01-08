import os
import telebot
from flask import Flask
from threading import Thread

# 1. Flask सेटअप (Render को ऑनलाइन रखने के लिए)
app = Flask('')
@app.route('/')
def home():
    return "Bot is Active!"

def run():
    app.run(host='0.0.0.0', port=10000)

# 2. Telegram Bot सेटअप
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- आपके पुराने सभी फीचर्स ---

# Start Command
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_text = (
        "नमस्ते रोशन! आपका ऑल-इन-वन AI बॉट तैयार है।\n\n"
        "मैं आपकी इन कामों में मदद कर सकता हूँ:\n"
        "1. सवालों के जवाब देना\n"
        "2. आपकी सर्विस को लाइव रखना\n"
        "3. लोकेशन और डिवाइस ट्रैकिंग\n"
        "4. ब्रॉडकास्ट मैसेज भेजना"
    )
    bot.reply_to(message, welcome_text)

# Location/IP Track Feature
@bot.message_handler(commands=['track'])
def track_feature(message):
    track_msg = (
        "🌐 IP: [Searching...]\n"
        "🏢 ISP: Checking Service...\n"
        "📱 Device: Linux aarch64\n"
        "🤖 Browser: Mozilla/5.0\n"
        "📍 Location: [Open in Google Maps]\n\n"
        "🤠 create by Roshan ali🤗"
    )
    bot.reply_to(message, track_msg)

# Broadcast Mode
@bot.message_handler(commands=['broadcast'])
def broadcast_feature(message):
    bot.reply_to(message, "📢 BROADCAST MODE\n\nवह मैसेज लिखें जो आप सभी यूजर्स को भेजना चाहते हैं:")

# जनरल मैसेज रिप्लाई
@bot.message_handler(func=lambda message: True)
def handle_all(message):
    bot.reply_to(message, f"आपने कहा: {message.text}")

# --- फीचर्स खत्म ---

def start_bot():
    # Conflict रोकने के लिए
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    t = Thread(target=run)
    t.start()
    print("Your full feature bot is starting...")
    start_bot()
    
