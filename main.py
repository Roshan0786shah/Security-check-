import os
import telebot
from flask import Flask
from threading import Thread

# 1. Flask सेटअप (Render को एक्टिव रखने के लिए)
app = Flask('')

@app.route('/')
def home():
    return "I am alive and running!"

def run():
    # Render इसी पोर्ट (10000) पर चेक करता है
    app.run(host='0.0.0.0', port=10000)

# 2. Telegram Bot सेटअप
TOKEN = os.environ.get('BOT_TOKEN') # इसे Render के Environment Variables में सेव करें
bot = telebot.TeleBot(TOKEN)

# --- यहाँ आपके सारे फीचर्स आएंगे ---

# स्वागत मैसेज (Start Command)
@bot.message_handler(commands=['start'])
def welcome(message):
    help_text = (
        "नमस्ते रोशन! आपका ऑल-इन-वन AI बॉट तैयार है।\n\n"
        "मैं आपकी इन कामों में मदद कर सकता हूँ:\n"
        "1. सवालों के जवाब देना\n"
        "2. आपकी सर्विस को लाइव रखना\n"
        "3. और भी बहुत कुछ!"
    )
    bot.reply_to(message, help_text)

# हेल्प कमांड
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.reply_to(message, "आपको क्या मदद चाहिए? बस टाइप करें!")

# जनरल मैसेज हैंडलर (जो भी आप लिखेंगे, बॉट उसका जवाब देगा)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    # यहाँ आप अपना AI लॉजिक जोड़ सकते हैं
    user_text = message.text.lower()
    
    if "kaise ho" in user_text:
        bot.reply_to(message, "मैं ठीक हूँ रोशन, आप कैसे हैं?")
    else:
        bot.reply_to(message, f"आपने कहा: {message.text}")

# --- फीचर्स खत्म ---

# 3. बॉट को बिना रुके चलाने का तरीका (Infinity Polling)
def start_bot():
    # यह Conflict (409) एरर को रोकने में मदद करता है
    bot.infinity_polling(timeout=10, long_polling_timeout=5)

if __name__ == "__main__":
    print("Starting Web Server...")
    t = Thread(target=run)
    t.start()
    
    print("Starting Telegram Bot...")
    # इससे 'Your service is live' वाला स्टेटस बना रहेगा
    start_bot()
    
