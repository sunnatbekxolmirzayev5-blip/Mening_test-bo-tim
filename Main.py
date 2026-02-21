import telebot
from telebot import types
from fpdf import FPDF
import google.generativeai as genai
import os
import time

# --- SOZLAMALAR ---
TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
GEMINI_KEY = 'AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw' # O'zingizning API kalitingizni qo'ying

bot = telebot.TeleBot(TOKEN)
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

class KursIshiPDF(FPDF):
    def header(self):
        if self.page_no() > 1:
            self.set_font('Arial', 'I', 8)
            self.cell(0, 10, 'Ilmiy kurs ishi - 2026', 0, 1, 'R')

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sahifa {self.page_no()}', 0, 0, 'C')

# --- ASOSIY MENYU ---
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(
        types.KeyboardButton("📘 40 Betlik Kurs ishi yaratish"),
        types.KeyboardButton("📝 Mustaqil ish tayyorlash"),
        types.KeyboardButton("📽 Slayd matnlarini tuzish")
    )
    bot.send_message(message.chat.id, f"Assalomu alaykum, {message.from_user.first_name}! 👋\nMen sizga darslik darajasidagi mukkammal ishlar tayyorlab beraman.", reply_markup=markup)

# --- MATN GENERATSIYASI (ZANJIR USULI) ---
def get_ai_content(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except:
        return "Tizimda yuklama yuqori, birozdan so'ng ushbu qism to'ldiriladi."

def generate_pro_work(message, work_type):
    topic = message.text
    status_msg = bot.send_message(message.chat.id, f"🚀 {work_type} tayyorlanmoqda...\nMatn takrorlanmasligi uchun har bir sahifa alohida yozilmoqda. (2-3 daqiqa kuting)")
    
    pdf = KursIshiPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    
    # 1. TITUL VARAG'I (Siz yuborgan namuna asosida)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.multi_cell(0, 10, "O'ZBEKISTON RESPUBLIKASI\nOLIY VA O'RTA MAXSUS TA'LIM VAZIRLIGI\nO'RTA MAXSUS, KASB-HUNAR TA'LIMI MARKAZI", 0, 'C')
    pdf.ln(60)
    pdf.set_font("Arial", 'B', 24)
    pdf.multi_cell(0, 15, topic.upper(), 0, 'C')
    pdf.ln(20)
    pdf.set_font("Arial", '', 18)
    pdf.cell(0, 10, work_type.upper(), 0, 1, 'C')
    pdf.ln(80)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "TOSHKENT - 2026", 0, 1, 'C')

    # 2. MUNDARIJA
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "MUNDARIJA", 0, 1, 'C')
    pdf.ln(10)
    sections = [
        ("KIRISH (Mavzu dolzarbligi va metodlar)", 3),
        ("I-BOB. NAZARIY VA USLUBIY ASOSLAR", 8),
        ("1.1. Sohaning rivojlanish tarixi", 14),
        ("1.2. Xorijiy davlatlar tajribasi", 20),
        ("II-BOB. AMALIY TAHLIL VA MUAMMOLAR", 26),
        ("2.1. O'zbekistondagi hozirgi holat", 32),
        ("XULOSA VA TAKLIFLAR", 38),
        ("FOYDALANILGAN ADABIYOTLAR", 40)
    ]
    pdf.set_font("Arial", '', 12)
    for title, pg in sections:
        pdf.cell(160, 10, title, 0, 0)
        pdf.cell(30, 10, str(pg), 0, 1, 'R')

    # 3. HAR BIR SAHIFA UCHUN ALOHIDA AI SO'ROVI (40 bet uchun)
    for title, _ in sections:
        # Har bir bo'lim uchun kamida 4-5 sahifa ma'lumot so'raymiz
        for i in range(1, 6): 
            pdf.add_page()
            pdf.set_font("Arial", 'B', 14)
            pdf.cell(0, 10, f"{title} (davomi {i})", 0, 1, 'L')
            pdf.ln(5)
            pdf.set_font("Arial", '', 12)
            
            # AIga juda qat'iy buyruq:
            prompt = f"'{topic}' mavzusida {title} bo'limining {i}-qismi uchun ilmiy, akademik va o'ta mukkammal matn yoz. Hech qaysi so'z oldingilari bilan takrorlanmasin. Kamida 500 ta so'z bo'lsin."
            matn = get_ai_content(prompt)
            pdf.multi_cell(0, 10, matn)
            time.sleep(1) # API block bo'lib qolmasligi uchun

    file_name = f"{message.chat.id}_mukkammal_ish.pdf"
    pdf.output(file_name)
    
    with open(file_name, 'rb') as f:
        bot.send_document(message.chat.id, f, caption=f"✅ {topic} mavzusidagi 40 betlik mukkammal ilmiy ish tayyorlandi!")
    
    os.remove(file_name)
    bot.delete_message(message.chat.id, status_msg.message_id)

# --- HABARLARNI QABUL QILISH ---
@bot.message_handler(func=lambda m: m.text == "📘 40 Betlik Kurs ishi yaratish")
def kurs_ishi(message):
    msg = bot.send_message(message.chat.id, "Kurs ishi mavzusini yuboring:")
    bot.register_next_step_handler(msg, lambda m: generate_pro_work(m, "Kurs ishi"))

@bot.message_handler(func=lambda m: m.text == "📝 Mustaqil ish tayyorlash")
def mustaqil_ish(message):
    msg = bot.send_message(message.chat.id, "Mustaqil ish mavzusini yuboring:")
    bot.register_next_step_handler(msg, lambda m: generate_pro_work(m, "Mustaqil ish"))

@bot.message_handler(func=lambda m: m.text == "📽 Slayt matnlarini tuzish")
def slayt(message):
    msg = bot.send_message(message.chat.id, "Slayt (taqdimot) mavzusini yuboring:")
    bot.register_next_step_handler(msg, generate_slide_content)

def generate_slide_content(message):
    topic = message.text
    bot.send_message(message.chat.id, "⏳ 7 ta slayd matni tayyorlanmoqda...")
    prompt = f"'{topic}' mavzusida 7 ta slayd uchun mukkammal matn yoz. Har bir slayd sarlavhasi, asosiy tezislar va xulosadan iborat bo'lsin."
    res = get_ai_content(prompt)
    bot.send_message(message.chat.id, res)

bot.infinity_polling()

