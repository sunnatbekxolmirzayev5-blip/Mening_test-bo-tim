import telebot
from telebot import types
from fpdf import FPDF
import google.generativeai as genai
import os
import time

# --- SOZLAMALAR ---
TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
GEMINI_KEY = 'AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw' # O'zingiz olgan kalitni qo'ying
ADMIN_ID =8016405262 # O'zingizning Telegram ID raqamingizni yozing

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

class PDF(FPDF):
    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sahifa {self.page_no()}', 0, 0, 'C')

# --- ASOSIY MENYU ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton("📘 Kurs ishi (PDF)")
    btn2 = types.KeyboardButton("📽 Slayt uchun tekst")
    btn3 = types.KeyboardButton("📝 Mustaqil ish")
    markup.add(btn1, btn2, btn3)
    
    if message.from_user.id == ADMIN_ID:
        admin_btn = types.KeyboardButton("⚙ Admin Panel")
        markup.add(admin_btn)

    bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}! 👋\nNamuna asosida mukkammal ish tayyorlaymiz. Yo'nalishni tanlang:", reply_markup=markup)

# --- KURS ISHI (PDF) JARAYONI ---
@bot.message_handler(func=lambda m: m.text == "📘 Kurs ishi (PDF)")
def ask_pdf_topic(message):
    msg = bot.send_message(message.chat.id, "Kurs ishi mavzusini yuboring:")
    bot.register_next_step_handler(msg, generate_full_pdf)

def generate_full_pdf(message):
    topic = message.text
    status = bot.send_message(message.chat.id, "🧠 AI tahlil qilmoqda va matn yozmoqda. Bu 1 daqiqa vaqt olishi mumkin...")
    
    pdf = PDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. Titul (Namuna:)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.multi_cell(0, 10, "O'ZBEKISTON RESPUBLIKASI\nOLIY VA O'RTA MAXSUS TA'LIM VAZIRLIGI\nO'RTA MAXSUS, KASB-HUNAR TA'LIMI MARKAZI", 0, 'C')
    pdf.ln(50)
    pdf.set_font("Arial", 'B', 20)
    pdf.multi_cell(0, 15, topic.upper(), 0, 'C')
    pdf.ln(80)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "TOSHKENT - 2026", 0, 1, 'C')

    # 2. AI dan har bir bo'lim uchun alohida va uzun matn olish
    sections = {
        "KIRISH": "Mavzuning dolzarbligi, maqsadi va vazifalari haqida 3 betlik ilmiy matn yoz.",
        "I-BOB. NAZARIY QISM": f"{topic} sohasining nazariy asoslari va olimlarning qarashlari haqida 15 betlik juda uzun matn yoz.",
        "II-BOB. AMALIY TAHLIL": f"{topic} ning hozirgi holati va muammolari haqida 15 betlik tahliliy matn yoz.",
        "XULOSA": "Olingan natijalar va takliflar haqida 5 betlik matn yoz."
    }

    for title, prompt in sections.items():
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(5)
        pdf.set_font("Arial", '', 12)
        
        try:
            response = model.generate_content(prompt)
            pdf.multi_cell(0, 10, response.text)
        except:
            pdf.multi_cell(0, 10, "Ma'lumot generatsiya qilishda xatolik yuz berdi.")

    file_name = f"{message.chat.id}_kursishi.pdf"
    pdf.output(file_name)
    
    with open(file_name, 'rb') as f:
        bot.send_document(message.chat.id, f, caption=f"✅ {topic} mavzusidagi mukkammal kurs ishi tayyor!")
    
    os.remove(file_name)
    bot.delete_message(message.chat.id, status.message_id)

# --- SLAYT VA MUSTAQIL ISH (TEXT) ---
@bot.message_handler(func=lambda m: m.text in ["📽 Slayt uchun tekst", "📝 Mustaqil ish"])
def handle_text_tasks(message):
    task = message.text
    msg = bot.send_message(message.chat.id, f"{task} mavzusini yozing:")
    bot.register_next_step_handler(msg, generate_text_work, task)

def generate_text_work(message, task):
    topic = message.text
    bot.send_message(message.chat.id, "⏳ Tayyorlanmoqda...")
    
    prompt = f"'{topic}' mavzusida {task} uchun mukkammal va kengaytirilgan matn tayyorlab ber."
    response = model.generate_content(prompt)
    
    bot.send_message(message.chat.id, response.text)

# --- ADMIN PANEL ---
@bot.message_handler(func=lambda m: m.text == "⚙ Admin Panel" and m.from_user.id == ADMIN_ID)
def admin_panel(message):
    bot.send_message(ADMIN_ID, "Xush kelibsiz Admin! Bot hozircha 100% onlayn holatda.")

bot.infinity_polling()
