import telebot
from telebot import types
from flask import Flask
import threading
import os

# --- Render के लिए सर्वर (इसे मत हटाना) ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Alive!"
def run():
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

# --- आपका असली बॉट कोड ---
API_TOKEN = '7607380112:AAFqTInE7pX0N_3A76uF85nS_m0_8_jH8uM' #
bot = telebot.TeleBot(API_TOKEN)

CHANNEL_ID = 'HackersColony' 
WEBSITE_URL = "https://roshan0786shah.github.io/Security-check-/"

def check_sub(user_id):
    try:
        status = bot.get_chat_member(f"@{CHANNEL_ID}", user_id).status
        return status in ['member', 'administrator', 'creator']
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    if check_sub(message.from_user.id):
        # पहले जैसा कीबोर्ड
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("🚀 LOCATION HACK"), types.KeyboardButton("🤖 CONTACT ADMIN"))
        markup.add(types.KeyboardButton("📢 BROADCAST"))
        bot.send_message(message.chat.id, f"✅ Welcome back {message.from_user.first_name}!\nSelect your tool below:", reply_markup=markup)
    else:
        # पहले जैसा Join बटन
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID}"))
        markup.add(types.InlineKeyboardButton("🔄 I joined", callback_data="check"))
        bot.send_message(message.chat.id, "❌ Access Denied!\nPlease join our channel to use this bot.", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_callback(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Success!")
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ You haven't joined yet!", show_alert=True)

@bot.message_handler(func=lambda message: message.text == "🚀 LOCATION HACK")
def loc_hack(message):
    msg = f"⚒ Tool Generated Successfully!\n\nCopy and send this link to your target:\n\n🔗 Your Link: {WEBSITE_URL}"
    bot.send_message(message.chat.id, msg)

if __name__ == "__main__":
    t = threading.Thread(target=run)
    t.daemon = True
    t.start()
    print("Bot is starting...")
    bot.infinity_polling(timeout=20, long_polling_timeout=10)
    
