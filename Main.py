import telebot
from telebot import types
from datetime import datetime
import random

# ⚠️ O'Z TOKENINGIZNI YOZING
API_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"

bot = telebot.TeleBot(API_TOKEN)

# Foydalanuvchi ma'lumotlarini saqlash
users = {}

# ======================
# START
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Kurs ishi yozish")

    bot.send_message(
        message.chat.id,
        "📚 25–40 punktli kurs ishi yozish botiga xush kelibsiz!\n\n"
        "Boshlash uchun tugmani bosing.",
        reply_markup=markup
    )

# ======================
# Xizmat tanlash
# ======================
@bot.message_handler(func=lambda m: m.text == "📚 Kurs ishi yozish")
def ask_topic(message):
    msg = bot.send_message(message.chat.id, "📌 Kurs ishi MAVZUSINI yozing:")
    bot.register_next_step_handler(msg, ask_name)

def ask_name(message):
    users[message.chat.id] = {}
    users[message.chat.id]["topic"] = message.text
    msg = bot.send_message(message.chat.id, "👤 Ism Familiyangizni yozing:")
    bot.register_next_step_handler(msg, ask_group)

def ask_group(message):
    users[message.chat.id]["name"] = message.text
    msg = bot.send_message(message.chat.id, "🎓 Guruhingizni yozing:")
    bot.register_next_step_handler(msg, generate_course)

# ======================
# Kurs ishini yaratish
# ======================
def generate_course(message):
    chat_id = message.chat.id
    users[chat_id]["group"] = message.text

    topic = users[chat_id]["topic"]
    name = users[chat_id]["name"]
    group = users[chat_id]["group"]
    year = datetime.now().year

    # 25–40 punkt yaratish
    num_points = random.randint(25, 40)
    points = [f"{i+1}. {topic} bilan bog‘liq muhim jihat №{i+1}" for i in range(num_points)]
    points_text = "\n".join(points)

    text = f"""
📚 *KURS ISHI*

*Mavzu:* {topic}

*Bajardi:* {name}  
*Guruh:* {group}  
*Yil:* {year}

--------------------------------------

*Kurs ishining 25–40 punktli tahlili:*

{points_text}

--------------------------------------

*XULOSA*

Yuqoridagi {num_points} punkt asosida {topic} mavzusi chuqur o‘rganildi.
Nazariy va amaliy jihatlar o‘rganildi va kelgusida rivojlantirish imkoniyatlari mavjud.

--------------------------------------

*FOYDALANILGAN ADABIYOTLAR*

1. Darslik va o‘quv qo‘llanmalar  
2. Ilmiy maqolalar  
3. Internet manbalari
"""

    bot.send_message(chat_id, text, parse_mode="Markdown")
    bot.send_message(chat_id, "✅ Kurs ishi tayyor! /start orqali qayta boshlashingiz mumkin.")

    users.pop(chat_id)

# ======================
# Noma'lum xabar
# ======================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "❗ Iltimos tugmani bosing yoki /start yozing.")

# ======================
# Botni ishga tushirish
# ======================
if __name__ == "__main__":
    print("🚀 Kurs ishi bot ishga tushdi...")
    bot.infinity_polling()
