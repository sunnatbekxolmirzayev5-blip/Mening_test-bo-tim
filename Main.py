import telebot
from fpdf import FPDF
from datetime import datetime
import random

API_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"  # Bu yerga o‘z tokeningizni qo‘ying
bot = telebot.TeleBot(API_TOKEN)

users = {}

# Jumlalar va so‘zlar ro'yxati (uzun matn yaratish uchun)
sentences = [
    "Kirish qismi mavzuni umumiy tushuntiradi va ahamiyatini ko‘rsatadi.",
    "Nazariy qismda asosiy tushunchalar va printsiplar bayon qilinadi.",
    "Amaliy qismda misollar va tahlillar keltiriladi.",
    "Har bir bo‘lim mavzuga oid muhim jihatlarni o‘z ichiga oladi.",
    "Xulosa qismi o‘rganilgan nazariy va amaliy jihatlarni umumlashtiradi.",
    "Adabiyotlar ro‘yxati manbalarni ko‘rsatadi va tadqiqot ishonchliligini oshiradi.",
    "Tadqiqot natijalari kelajakda qo‘llanish imkoniyatlarini ko‘rsatadi.",
    "Har bir bo‘lim mavzuni chuqur tahlil qiladi va misollar bilan mustahkamlaydi."
]

# ======================
# Start komandasi
# ======================
@bot.message_handler(commands=['start'])
def start(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📚 Daftar to‘ldirish")
    bot.send_message(message.chat.id, "📚 12 varaqli yoki ko‘proq daftar botiga xush kelibsiz! Tugmani bosing.", reply_markup=markup)

# ======================
# Mavzu so‘rash
# ======================
@bot.message_handler(func=lambda m: m.text == "📚 Daftar to‘ldirish")
def ask_topic(message):
    msg = bot.send_message(message.chat.id, "📌 Daftar mavzusini yozing:")
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
# PDF yaratish (12 varaq yoki ko‘proq)
# ======================
def generate_pdf(message):
    chat_id = message.chat.id
    users[chat_id]["group"] = message.text

    topic = users[chat_id]["topic"]
    name = users[chat_id]["name"]
    group = users[chat_id]["group"]
    year = datetime.now().year

    num_pages = 12   # 12 varaq, xohlasa oshirish mumkin
    words_per_page = 5000  # Har varaqdagi so‘zlar soni
    # So‘zlarni to‘ldirish
    pages_text = []
    for _ in range(num_pages):
        page_text = " ".join([random.choice(sentences) for _ in range(words_per_page)])
        pages_text.append(page_text)

    # PDF yaratish
    pdf = FPDF(format='A4')
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", '', 12)

    for i, page_text in enumerate(pages_text, start=1):
        pdf.add_page()
        pdf.multi_cell(0, 8, f"Daftar - Varaq {i}\nMavzu: {topic}\nBajardi: {name}\nGuruh: {group}\nYil: {year}\n\n")
        pdf.multi_cell(0, 8, page_text)

    file_name = f"{chat_id}_daftar.pdf"
    pdf.output(file_name)

    with open(file_name, "rb") as f:
        bot.send_document(chat_id, f)

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
    print("🚀 Daftar bot ishga tushdi...")
    bot.infinity_polling()
