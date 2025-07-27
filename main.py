import telebot
import subprocess
import os
from deepai import DeepAI

# Keys
BOT_TOKEN = "8350091765:AAHvwltUWQzJn3xYg22gEHzRSIUEO-n32xA"
DEEPAI_KEY = "62ca4f9b-c097-46b3-ad2d-90ecf9631dbd"
OWNER_ID = 7983114161

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def greet(message):
    if message.chat.id != OWNER_ID:
        bot.send_message(message.chat.id, "Access Denied.")
        return
    bot.send_message(message.chat.id, "🛡 BinaryShield AI Bot Online. Monitoring...")

@bot.message_handler(commands=['check_voice'])
def check_voice(message):
    bot.send_message(OWNER_ID, "🎙 Send the voice message now for deepfake detection...")

@bot.message_handler(content_types=['voice'])
def handle_voice(message):
    if message.chat.id != OWNER_ID:
        return

    file_info = bot.get_file(message.voice.file_id)
    downloaded = bot.download_file(file_info.file_path)
    
    with open("voice.ogg", "wb") as f:
        f.write(downloaded)

    result = subprocess.getoutput(f"curl -F 'audio=@voice.ogg' -H 'api-key: {DEEPAI_KEY}' https://api.deepai.org/api/voice-detection")
    bot.send_message(OWNER_ID, f"DeepAI Result:\n{result}")

@bot.message_handler(commands=['scan'])
def binary_scan(message):
    output = subprocess.getoutput("find / -type f -perm -4000 2>/dev/null")
    bot.send_message(OWNER_ID, f"🔍 Suspicious binaries with SUID:\n{output[:4096]}")

@bot.message_handler(commands=['who'])
def whoami(message):
    out = subprocess.getoutput("whoami && id && uname -a")
    bot.send_message(OWNER_ID, f"🧠 System Info:\n{out}")

bot.polling(non_stop=True)