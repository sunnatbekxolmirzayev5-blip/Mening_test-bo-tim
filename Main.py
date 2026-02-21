import telebot
from telebot import types
from datetime import datetime
import random

API_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"
bot = telebot.TeleBot(API_TOKEN)

users = {}

# So‘zlar ro‘yxati (matnni uzun qiladigan)
words = [
    "kirish", "tahlil", "nazariya", "misol", "chiqish", 
    "natija", "xulosa", "tajriba", "o‘rganish", "ma’lumot",
    "o‘zlashtirish", "ilmiy", "amaliy", "ilm", "tadqiqot"
]

# ======================
# START
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Kurs ishi yozish")
    bot.send_message(
        message.chat.id,
        "📚 Kurs ishi botiga xush kelibsiz! Boshlash uchun tugmani bosing.",
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

    # Matnni generatsiya qilish
    total_words = 400000
    text_list = []
    for i in range(total_words):
        text_list.append(random.choice(words))
    
    # Matnni bo‘laklarga bo‘lish (Telegram xabar chegarasi ~4000 belgi)
    text_chunks = []
    chunk_size = 4000
    full_text = " ".join(text_list)
    for i in range(0, len(full_text), chunk_size):
        text_chunks.append(full_text[i:i+chunk_size])

    # Kirish qismi
    intro = f"""
📚 *KURS ISHI*

*Mavzu:* {topic}
*Bajardi:* {name}
*Guruh:* {group}
*Yil:* {year}

--------------------------------------
*Kirish*
Ushbu kurs ishi mavzu bo‘yicha chuqur tahlil va amaliy tadqiqotlarni o‘z ichiga oladi.
"""
    bot.send_message(chat_id, intro, parse_mode="Markdown")

    # Matn bo‘laklarini yuborish
    for chunk in text_chunks:
        bot.send_message(chat_id, chunk)

    # Xulosa
    conclusion = """
--------------------------------------
*Xulosa*
Ushbu kurs ishida mavzu chuqur o‘rganildi. Nazariy va amaliy jihatlar tahlil qilindi.
--------------------------------------
*Foydalanilgan adabiyotlar*
1. Darslik va o‘quv qo‘llanmalar
2. Ilmiy maqolalar
3. Internet manbalari
"""
    bot.send_message(chat_id, conclusion, parse_mode="Markdown")
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
