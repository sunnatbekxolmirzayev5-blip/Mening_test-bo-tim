import telebot
from telebot import types
from fpdf import FPDF
import google.generativeai as genai
import os
import time

# --- SOZLAMALAR ---
TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
GEMINI_KEY = 'AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw' 

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

class KursIshiPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Ilmiy tadqiqot ishi - 2026', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sahifa {self.page_no()}', 0, 0, 'C')

def safe_ai_generate(prompt):
    """AI javob bermasa 3 marta qayta urinib ko'radigan funksiya"""
    for _ in range(3):
        try:
            response = model.generate_content(prompt)
            if response.text:
                return response.text
        except:
            time.sleep(2)
    return "Ushbu bo'lim bo'yicha ilmiy tahlillar davom etmoqda. Batafsil ma'lumot ilova qilinadi."

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📘 Mukkammal 40 betlik Kurs ishi")
    bot.send_message(message.chat.id, "Mavzuni yuboring, men uni 40 betlik ilmiy asarga aylantiraman.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📘 Mukkammal 40 betlik Kurs ishi")
def get_topic(message):
    msg = bot.send_message(message.chat.id, "Kurs ishi mavzusini aniq yozing:")
    bot.register_next_step_handler(msg, generate_full_document)

def generate_full_document(message):
    topic = message.text
    status = bot.send_message(message.chat.id, "⌛️ Diqqat! 40 betlik matn tayyorlanmoqda. Bu jarayon 3-5 daqiqa olishi mumkin. Iltimos, kutib turing...")
    
    pdf = KursIshiPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # 1. TITUL (Siz yuborgan namunadagi kabi)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.multi_cell(0, 10, "O'ZBEKISTON RESPUBLIKASI\nOLIY TA'LIM, FAN VA INNOVATSIYALAR VAZIRLIGI", 0, 'C')
    pdf.ln(50)
    pdf.set_font("Arial", 'B', 24)
    pdf.multi_cell(0, 15, topic.upper(), 0, 'C')
    pdf.ln(20)
    pdf.set_font("Arial", '', 14)
    pdf.cell(0, 10, "KURS ISHI", 0, 1, 'C')
    pdf.ln(80)
    pdf.cell(0, 10, "TOSHKENT - 2026", 0, 1, 'C')

    # Bo'limlar rejasini tuzish
    structure = [
        ("KIRISH", "Mavzuning dolzarbligi, maqsadi, vazifalari va ilmiy yangiligi haqida 4 betlik matn."),
        ("I-BOB. NAZARIY ASOSLAR", f"{topic} mavzusining nazariy asosi, xorij olimlarining fikrlari va adabiyotlar tahlili haqida 12 betlik matn."),
        ("II-BOB. AMALIY TAHLIL", f"{topic}ning O'zbekistondagi bugungi holati, raqamlar va muammolar haqida 14 betlik tahliliy matn."),
        ("XULOSA VA TAKLIFLAR", "Tadqiqot natijasida olingan 10 ta muhim xulosa va amaliy tavsiyalar (6 bet)."),
        ("ADABIYOTLAR RO'YXATI", "Kamida 20 ta eng so'nggi ilmiy adabiyotlar ro'yxati (2020-2025 yillar).")
    ]

    # 2. HAR BIR BO'LIMNI GENERATSIYA QILISH
    for title, prompt_desc in structure:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'C')
        pdf.ln(5)
        pdf.set_font("Arial", '', 12)
        
        # Har bir bo'limni 3 bo'lakka bo'lib so'raymiz (uzunroq bo'lishi uchun)
        for part in range(1, 4):
            full_prompt = f"Siz akademik professosiz. {topic} mavzusida {title} qismi uchun {prompt_desc}. Bu {part}-bo'lak. Juda batafsil, ilmiy tilda, takrorlanmas gaplar bilan yozing."
            content = safe_ai_generate(full_prompt)
            pdf.multi_cell(0, 10, content)
            time.sleep(1) # API limitdan himoya

    file_name = f"{topic}_40_betlik.pdf"
    pdf.output(file_name)
    
    with open(file_name, 'rb') as f:
        bot.send_document(message.chat.id, f, caption=f"✅ Mukkammal ish tayyor! \nMavzu: {topic}\nHajmi: 40 bet atrofida.")
    
    os.remove(file_name)
    bot.delete_message(message.chat.id, status.message_id)

bot.infinity_polling()
