import telebot
from telebot import types
from datetime import datetime

# ⚠️ O'Z TOKENINGIZNI YOZING
API_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"

bot = telebot.TeleBot(API_TOKEN)

# Foydalanuvchi ma'lumotlarini saqlash
users = {}

# =========================
# START
# =========================
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("📚 Kurs ishi yozish")
    markup.add(btn)

    bot.send_message(
        message.chat.id,
        "📚 Kurs ishi yozish botiga xush kelibsiz!\n\n"
        "Boshlash uchun tugmani bosing.",
        reply_markup=markup
    )

# =========================
# Xizmat tanlash
# =========================
@bot.message_handler(func=lambda m: m.text == "📚 Kurs ishi yozish")
def get_topic(message):
    msg = bot.send_message(message.chat.id, "📌 Kurs ishi MAVZUSINI yozing:")
    bot.register_next_step_handler(msg, get_name)

def get_name(message):
    users[message.chat.id] = {}
    users[message.chat.id]["topic"] = message.text

    msg = bot.send_message(message.chat.id, "👤 Ism Familiyangizni yozing:")
    bot.register_next_step_handler(msg, get_group)

def get_group(message):
    users[message.chat.id]["name"] = message.text

    msg = bot.send_message(message.chat.id, "🎓 Guruhingizni yozing:")
    bot.register_next_step_handler(msg, generate_course)

# =========================
# Kurs ishi yaratish
# =========================
def generate_course(message):
    chat_id = message.chat.id
    users[chat_id]["group"] = message.text

    topic = users[chat_id]["topic"]
    name = users[chat_id]["name"]
    group = users[chat_id]["group"]
    year = datetime.now().year

    text = f"""
📚 KURS ISHI

Mavzu: {topic}

Bajardi: {name}
Guruh: {group}
Yil: {year}

--------------------------------------

KIRISH

Ushbu kurs ishida "{topic}" mavzusi batafsil o‘rganiladi.
Mazkur mavzu hozirgi kunda dolzarb hisoblanadi va
ilmiy-amaliy ahamiyatga ega.

--------------------------------------

I-BOB. NAZARIY ASOSLAR

{topic} tushunchasi, uning mazmuni va rivojlanish
bosqichlari tahlil qilinadi.
Asosiy ilmiy qarashlar va nazariy manbalar ko‘rib chiqiladi.

--------------------------------------

II-BOB. AMALIY TAHLIL

Amaliy misollar va real ma’lumotlar asosida
{topic} tahlil qilinadi.
Muammolar va ularning yechimlari bayon etiladi.

--------------------------------------

XULOSA

Yuqoridagi tahlillar asosida quyidagi xulosalarga kelindi:

- {topic} muhim ilmiy yo‘nalish hisoblanadi.
- Nazariy va amaliy jihatlar bir-birini to‘ldiradi.
- Kelajakda rivojlantirish imkoniyatlari mavjud.

--------------------------------------

FOYDALANILGAN ADABIYOTLAR

1. Darslik va o‘quv qo‘llanmalar
2. Ilmiy maqolalar
3. Internet manbalari
"""

    bot.send_message(chat_id, text)
    bot.send_message(chat_id, "✅ Kurs ishi tayyor! Yana boshlash uchun /start ni bosing.")

    users.pop(chat_id)

# =========================
# Noma'lum xabar
# =========================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "❗ Iltimos tugmani bosing yoki /start yozing.")

# =========================
# Botni ishga tushirish
# =========================
if __name__ == "__main__":
    print("🚀 Bot ishga tushdi...")
    bot.infinity_polling()
