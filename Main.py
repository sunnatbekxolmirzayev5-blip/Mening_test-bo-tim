import telebot
from fpdf import FPDF
from datetime import datetime
import random
import os

API_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"  # Bu yerga o‘z tokeningizni qo‘ying
bot = telebot.TeleBot(API_TOKEN)

users = {}

# Jumla va paragraf ro'yxati (uzun matn yaratish uchun)
sentences = [
    "Kirish qismi mavzuni umumiy tushuntiradi va ahamiyatini ko‘rsatadi.",
    "Nazariy qismda asosiy tushunchalar va printsiplar bayon qilinadi.",
    "Amaliy qismda misollar va tahlillar keltiriladi.",
    "Har bir bo‘lim mavzuga oid muhim jihatlarni o‘z ichiga oladi.",
    "Xulosa qismi o‘rganilgan nazariy va amaliy jihatlarni umumlashtiradi.",
    "Adabiyotlar ro‘yxati manbalarni ko‘rsatadi va tadqiqot ishonchliligini oshiradi.",
    "Tadqiqot natijalari kelajakda qo‘llanish imkoniyatlarini ko‘rsatadi.",
    "Har bir bo‘lim mavzuni chuqur tahlil qiladi va misollar bilan mustahkamlaydi.",
    "Bu mavzu bo‘yicha tadqiqot va tahlillar muhim ahamiyatga ega.",
    "Matn har bir varaqda mukammal tarzda joylashtiriladi.",
    "Kurs ishida nazariy va amaliy jihatlar o‘rganildi.",
    "Ilmiy tadqiqotlar mavzuning ahamiyatini kuchaytiradi.",
    "Har bir bo‘lim batafsil tahlil va misollar bilan boyitiladi.",
    "Bu mavzuning ilmiy ahamiyati katta."
]

# ======================
# Start komandasi
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Katta Kitob")
    bot.send_message(message.chat.id, "📚 Katta kitob PDF botga xush kelibsiz! Tugmani bosing.", reply_markup=markup)

# ======================
# Mavzu so‘rash
# ======================
@bot.message_handler(func=lambda m: m.text == "📚 Katta Kitob")
def ask_topic(message):
    msg = bot.send_message(message.chat.id, "📌 Kitob mavzusini yozing:")
    bot.register_next_step_handler(msg, ask_name)

def ask_name(message):
    users[message.chat.id] = {}
    users[message.chat.id]["topic"] = message.text
    msg = bot.send_message(message.chat.id, "👤 Ism Familiyangizni yozing:")
    bot.register_next_step_handler(msg, ask_group)

def ask_group(message):
    users[message.chat.id]["name"] = message.text
    msg = bot.send_message(message.chat.id, "🎓 Guruhingizni yozing:")
    bot.register_next_step_handler(msg, generate_pdf)

# ======================
# PDF yaratish (katta kitob)
# ======================
def generate_pdf(message):
    chat_id = message.chat.id
    users[chat_id]["group"] = message.text

    topic = users[chat_id]["topic"]
    name = users[chat_id]["name"]
    group = users[chat_id]["group"]
    year = datetime.now().year

    # ======================
    # Parametrlar
    # ======================
    num_pages = 100           # 100 varaq → katta kitob
    words_per_page = 10000    # Har varaq ~10k so‘z → jami ~1M so‘z

    # ======================
    # PDF yaratish
    # ======================
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", '', 12)

    for page in range(1, num_pages + 1):
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 10, f"Kitob - Varaq {page}\nMavzu: {topic}\nBajardi: {name}\nGuruh: {group}\nYil: {year}\n\n")
        pdf.set_font("Arial", '', 12)

        # Har varaq uchun random matn
        varaq_text = " ".join([random.choice(sentences) for _ in range(words_per_page)])
        pdf.multi_cell(0, 6, varaq_text)

    file_name = f"{chat_id}_katta_kitob.pdf"
    pdf.output(file_name)

    # Telegramga yuborish
    with open(file_name, "rb") as f:
        bot.send_document(chat_id, f)

    # Faylni o‘chirish (xotira tejash uchun)
    os.remove(file_name)
    users.pop(chat_id)

# ======================
# Fallback
# ======================
@bot.message_handler(func=lambda m: True)
def fallback(message):
    bot.send_message(message.chat.id, "❗ Iltimos tugmani bosing yoki /start yozing.")

# ======================
# Bot ishga tushirish
# ======================
if __name__ == "__main__":
    print("🚀 Katta kitob bot ishga tushdi...")
    bot.infinity_polling()
