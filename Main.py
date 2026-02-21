import telebot
from telebot import types
from fpdf import FPDF
import google.generativeai as genai
import os

# --- SOZLAMALAR ---
TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
GEMINI_KEY = 'AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw' # Gemini API kalitingiz
ADMIN_ID =8016405262  # @userinfobot bergan raqamni shu yerga qo'ying
ADMIN_USERNAME = "@Sizning_Loginingiz" # Telegram loginingiz (masalan: @uz_admin)

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
    btn2 = types.KeyboardButton("📝 Mustaqil ish (PDF)")
    btn3 = types.KeyboardButton("📽 Slayt (7-bet)")
    btn4 = types.KeyboardButton("👨‍💻 Admin bilan bog'lanish")
    markup.add(btn1, btn2, btn3, btn4)
    
    bot.send_message(message.chat.id, f"Salom {message.from_user.first_name}! 👋\nIsh turini tanlang. Men har birini takrorlanmas va mukkammal qilib tayyorlab beraman.", reply_markup=markup)

# --- PDF GENERATSIYA FUNKSIYASI ---
def generate_common_pdf(message, work_type, topic):
    status = bot.send_message(message.chat.id, "🧠 AI ma'lumotlarni tahlil qilmoqda. Bu biroz vaqt olishi mumkin (1-2 daqiqa)...")
    
    try:
        pdf = PDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        
        # Titul varag'i (Namunangiz asosida)
        pdf.add_page()
        pdf.set_font("Arial", 'B', 14)
        pdf.multi_cell(0, 10, "O'ZBEKISTON RESPUBLIKASI\nOLIY VA O'RTA MAXSUS TA'LIM VAZIRLIGI\nO'RTA MAXSUS, KASB-HUNAR TA'LIMI MARKAZI", 0, 'C')
        pdf.ln(50)
        pdf.set_font("Arial", 'B', 20)
        pdf.multi_cell(0, 15, topic.upper(), 0, 'C')
        pdf.ln(20)
        pdf.set_font("Arial", '', 16)
        pdf.cell(0, 10, work_type.upper(), 0, 1, 'C')
        pdf.ln(80)
        pdf.set_font("Arial", '', 12)
        pdf.cell(0, 10, "TOSHKENT - 2026", 0, 1, 'C')

        # Bo'limlar ro'yxati
        sections = ["KIRISH", "I-BOB. NAZARIY QISM", "II-BOB. AMALIY TAHLIL", "XULOSA", "ADABIYOTLAR"]
        
        for section in sections:
            pdf.add_page()
            pdf.set_font("Arial", 'B', 16)
            pdf.cell(0, 10, section, 0, 1, 'C')
            pdf.ln(10)
            pdf.set_font("Arial", '', 12)
            
            # AI so'rovi (Takrorlanmaslik uchun har safar yangi prompt)
            prompt = f"'{topic}' mavzusida {work_type} uchun {section} qismini juda batafsil va ilmiy tilda yoz. Hech qaysi so'z va gap takrorlanmasin, mukkammal bo'lsin."
            response = model.generate_content(prompt)
            pdf.multi_cell(0, 10, response.text)

        file_path = f"{message.chat.id}_work.pdf"
        pdf.output(file_path)
        
        with open(file_path, 'rb') as f:
            bot.send_document(message.chat.id, f, caption=f"✅ {topic} mavzusidagi {work_type} tayyor!")
        
        os.remove(file_path)
        bot.delete_message(message.chat.id, status.message_id)

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Xatolik yuz berdi! Tizim yuklamani ko'tara olmadi yoki API kalitda muammo bor.\n\nIltimos, adminga xabar bering: {ADMIN_USERNAME}")

# --- HABARLARNI BOSHQARISH ---
@bot.message_handler(func=lambda m: m.text in ["📘 Kurs ishi (PDF)", "📝 Mustaqil ish (PDF)"])
def start_pdf_process(message):
    work_type = message.text
    msg = bot.send_message(message.chat.id, f"{work_type} mavzusini yuboring:")
    bot.register_next_step_handler(msg, lambda m: generate_common_pdf(m, work_type, m.text))

@bot.message_handler(func=lambda m: m.text == "📽 Slayt (7-bet)")
def start_slide_process(message):
    msg = bot.send_message(message.chat.id, "Slayt (taqdimot) mavzusini yuboring:")
    bot.register_next_step_handler(msg, generate_slide_text)

def generate_slide_text(message):
    try:
        topic = message.text
        bot.send_message(message.chat.id, "⏳ 7 ta slaydlik mukkammal matn tayyorlanmoqda...")
        prompt = f"'{topic}' mavzusida taqdimot uchun 7 ta alohida slayd tayyorla. Har bir slaydning sarlavhasi va ichidagi matni alohida bo'lsin. Takrorlanishlar bo'lmasin."
        response = model.generate_content(prompt)
        bot.send_message(message.chat.id, response.text)
    except:
        bot.send_message(message.chat.id, f"❌ Slayt yaratishda xatolik! Adminga murojaat qiling: {ADMIN_USERNAME}")

@bot.message_handler(func=lambda m: m.text == "👨‍💻 Admin bilan bog'lanish")
def admin_contact(message):
    bot.send_message(message.chat.id, f"Savollar, takliflar va xatoliklar bo'yicha adminga yozishingiz mumkin:\n👉 {ADMIN_USERNAME}")

bot.infinity_polling()
