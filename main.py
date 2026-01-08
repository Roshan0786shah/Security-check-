import telebot
from telebot import types
from flask import Flask
import threading
import os

# --- Flask सेटअप (Render के Port Error को ठीक करने के लिए) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is Running!"

def run():
    # Render द्वारा दिए गए पोर्ट पर सर्वर चलाना
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# --- टेलीग्राम बॉट सेटअप ---
API_TOKEN = '8341294834:AAGDMuDZJ8ZYtC6QPnF_3KH_aRJ3wXyg_w0' # आपका टोकन
bot = telebot.TeleBot(API_TOKEN)

CHANNEL_ID = 'HackersColony' 
WEBSITE_URL = "https://roshan0786shah.github.io/Security-check-/"

def check_sub(user_id):
    try:
        status = bot.get_chat_member(f"@{CHANNEL_ID}", user_id).status
        return status in ['member', 'administrator', 'creator']
    except:
        return False

@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🚀 LOCATION HACK"), types.KeyboardButton("🤖 CONTACT ADMIN"))
        bot.send_message(message.chat.id, f"✅ Welcome {message.from_user.first_name}!", reply_markup=markup)
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID}"))
        markup.add(types.InlineKeyboardButton("🔄 I joined", callback_data="check"))
        bot.send_message(message.chat.id, "❌ Please join our channel first!", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_callback(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Success!")
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ Join first!", show_alert=True)

@bot.message_handler(func=lambda message: message.text == "🚀 LOCATION HACK")
def loc_hack(message):
    bot.send_message(message.chat.id, f"🔗 Your Link: {WEBSITE_URL}")

# --- मुख्य हिस्सा (Main Execution) ---
if __name__ == "__main__":
    # Flask को अलग थ्रेड में चलाएं ताकि Render खुश रहे
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    
    print("Bot is starting...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
    
