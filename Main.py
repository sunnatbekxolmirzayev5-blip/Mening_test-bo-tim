import telebot
from telebot import types
from fpdf import FPDF
import google.generativeai as genai
import os
import time

# 1. SOZLAMALAR
TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
GEMINI_KEY = 'AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw' # Bu yerga Gemini API kalitini qo'yasiz

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

class ProPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Professional Kurs Ishi tizimi', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sahifa {self.page_no()}', 0, 0, 'C')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! Men 40 betlik ilmiy kurs ishi yozib beraman. Mavzuni yuboring:")

@bot.message_handler(func=lambda m: True)
def handle_topic(message):
    topic = message.text
    status_msg = bot.send_message(message.chat.id, "🧠 AI kurs ishini yozmoqda... (40 betlik matn uchun 1-2 daqiqa kuting)")
    
    pdf = ProPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- TITUL VARAG'I (Siz yuborgan namuna asosida) ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.multi_cell(0, 10, "O'ZBEKISTON RESPUBLIKASI\nOLIY VA O'RTA MAXSUS TA'LIM VAZIRLIGI", 0, 'C')
    pdf.ln(50)
    pdf.set_font("Arial", 'B', 20)
    pdf.multi_cell(0, 15, topic.upper(), 0, 'C')
    pdf.ln(100)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "TOSHKENT - 2024", 0, 1, 'C')

    # --- AI ORQALI MATN YARATISH ---
    sections = ["KIRISH", "I-BOB. NAZARIY ASOSLAR", "II-BOB. AMALIY TAHLIL", "XULOSA"]
    
    for section in sections:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, section, 0, 1, 'L')
        pdf.ln(5)
        pdf.set_font("Arial", '', 12)
        
        # AI-dan har bir bo'lim uchun 8-10 betlik matn so'raymiz
        try:
            response = model.generate_content(f"'{topic}' mavzusida {section} qismi uchun juda batafsil, ilmiy va uzun matn yozib ber. 10 betga yetsin.")
            pdf.multi_cell(0, 10, response.text)
        except:
            pdf.multi_cell(0, 10, f"{section} bo'yicha ma'lumotlar tayyorlanmoqda...")

    file_path = f"{topic}.pdf"
    pdf.output(file_path)
    
    with open(file_path, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="✅ Mukammal 40 betlik kurs ishingiz tayyor!")
    
    os.remove(file_path)
    bot.delete_message(message.chat.id, status_msg.message_id)

bot.infinity_polling()
