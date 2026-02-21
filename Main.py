import telebot
from telebot import types
from dotenv import load_dotenv
import os

# .env yuklash
load_dotenv()
API_TOKEN = os.getenv("8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg")

bot = telebot.TeleBot(API_TOKEN)

# Foydalanuvchi holatini saqlash
user_data = {}

# ==============================
# START
# ==============================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📽 Slayt tayyorlash", "📚 Kurs ishi tayyorlash")
    
    bot.send_message(
        message.chat.id,
        f"Salom {message.from_user.first_name}! 👋\n"
        "Xizmat turini tanlang:",
        reply_markup=markup
    )

# ==============================
# CANCEL
# ==============================
@bot.message_handler(commands=['cancel'])
def cancel(message):
    user_data.pop(message.chat.id, None)
    bot.send_message(message.chat.id, "❌ Bekor qilindi. /start ni bosing.")

# ==============================
# Xizmat tanlash
# ==============================
@bot.message_handler(func=lambda m: m.text in ["📽 Slayt tayyorlash", "📚 Kurs ishi tayyorlash"])
def choose_service(message):
    user_data[message.chat.id] = {"service": message.text}
    msg = bot.send_message(message.chat.id, "📌 Mavzuni yozing:")
    bot.register_next_step_handler(msg, generate_content)

# ==============================
# Kontent yaratish
# ==============================
def generate_content(message):
    chat_id = message.chat.id
    topic = message.text
    
    if chat_id not in user_data:
        bot.send_message(chat_id, "❗ Iltimos avval xizmat tanlang. /start")
        return
    
    service = user_data[chat_id]["service"]

    if service == "📽 Slayt tayyorlash":
        result = f"""
📽 *{topic}* mavzusida slayt rejasi:

1️⃣ Kirish va mavzu nomi  
2️⃣ Dolzarblik va maqsad  
3️⃣-5️⃣ Nazariy ma'lumotlar  
6️⃣-8️⃣ Tahlil va misollar  
9️⃣ Xulosa  
🔟 Foydalanilgan adabiyotlar
"""
    else:
        result = f"""
📚 *{topic}* mavzusida kurs ishi namunasi:

*КIRISH*  
Mavzuning dolzarbligi va maqsadi.

*I-BOB*  
Nazariy asoslar.

*II-BOB*  
Amaliy tahlil.

*XULOSA*  
Yakuniy fikr va takliflar.
"""

    bot.send_message(chat_id, result, parse_mode="Markdown")
    bot.send_message(chat_id, "✅ Tayyor! Yana davom etamizmi? /start")

    # Holatni tozalash
    user_data.pop(chat_id)

# ==============================
# Noma'lum xabar
# ==============================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "❗ Buyruq noto‘g‘ri. /start ni bosing.")

# ==============================
# BOTNI ISHGA TUSHIRISH
# ==============================
if __name__ == "__main__":
    bot.remove_webhook()
    print("🚀 Bot ishga tushdi...")
    bot.infinity_polling()
