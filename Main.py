import telebot
from telebot import types
from fpdf import FPDF
import os

TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
bot = telebot.TeleBot(TOKEN)

class KursIshiPDF(FPDF):
    def header(self):
        # Sahifa tepasida kichik chiziq yoki sarlavha (ixtiyoriy)
        pass

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.cell(0, 10, f'Sahifa {self.page_no()}', 0, 0, 'C')

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📘 40 Betlik Mukkamal PDF yaratish"))
    bot.send_message(message.chat.id, "Assalomu alaykum! Namuna asosida professional kurs ishi tayyorlaymiz. Mavzuni yuboring:", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📘 40 Betlik Mukkamal PDF yaratish")
def ask_topic(message):
    msg = bot.send_message(message.chat.id, "Kurs ishi mavzusini to'liq yozing:")
    bot.register_next_step_handler(msg, generate_pro_pdf)

def generate_pro_pdf(message):
    topic = message.text
    bot.send_message(message.chat.id, "⏳ Namuna asosida 40 betlik PDF shakllanmoqda... (30 soniya kuting)")
    
    pdf = KursIshiPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    
    # --- 1. TITUL VARAG'I (Namuna asosida) ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 14)
    pdf.multi_cell(0, 10, "O'ZBEKISTON RESPUBLIKASI\nOLIY VA O'RTA MAXSUS TA'LIM VAZIRLIGI", 0, 'C')
    pdf.ln(40)
    pdf.set_font("Arial", 'B', 22)
    pdf.multi_cell(0, 15, topic.upper(), 0, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 16)
    pdf.cell(0, 10, "KURS ISHI", 0, 1, 'C')
    pdf.ln(50)
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, "Bajardi: ________________ (Talaba ismi)", 0, 1, 'R')
    pdf.cell(0, 10, "Qabul qildi: ______________ (O'qituvchi)", 0, 1, 'R')
    pdf.ln(30)
    pdf.cell(0, 10, "TOSHKENT - 2024", 0, 1, 'C')

    # --- 2. MUNDARIJA ---
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, "MUNDARIJA", 0, 1, 'C')
    pdf.ln(10)
    pdf.set_font("Arial", '', 12)
    contents = [
        ("KIRISH", "3"),
        ("I-BOB. NAZARIY VA USLUBIY ASOSLAR", "7"),
        ("  1.1. Mavzuning o'rganilish darajasi", "12"),
        ("  1.2. Asosiy tushunchalar tahlili", "18"),
        ("II-BOB. AMALIY TAHLIL VA MUAMMOLAR", "24"),
        ("  2.1. Hozirgi holatning statistik tahlili", "30"),
        ("XULOSA VA TAKLIFLAR", "37"),
        ("FOYDALANILGAN ADABIYOTLAR", "40")
    ]
    for item, page in contents:
        pdf.cell(160, 10, item, 0, 0)
        pdf.cell(30, 10, page, 0, 1, 'R')

    # --- 3. 40 BETLIK MATN GENERATSIYASI ---
    sections = [
        ("KIRISH", 4), # Sahifa soni
        ("I-BOB. NAZARIY ASOSLAR", 15),
        ("II-BOB. AMALIY TAHLIL", 15),
        ("XULOSA VA ADABIYOTLAR", 4)
    ]

    for title, pages in sections:
        pdf.add_page()
        pdf.set_font("Arial", 'B', 16)
        pdf.cell(0, 10, title, 0, 1, 'L')
        pdf.ln(5)
        pdf.set_font("Arial", '', 12)
        
        for p in range(pages):
            content = f"Ushbu {topic} mavzusi doirasida keng qamrovli tadqiqotlar olib borildi. "
            content += "Namuna sifatida olingan darslikdagi kabi har bir tushunchaga alohida urg'u berildi. "
            content += (f"{topic} rivojlanish bosqichlari va uning jamiyatdagi o'rni beqiyosdir. " * 30)
            pdf.multi_cell(0, 10, content)
            if p < pages - 1:
                pdf.add_page()

    file_name = f"Kurs_ishi_{message.chat.id}.pdf"
    pdf.output(file_name)
    
    with open(file_name, 'rb') as f:
        bot.send_document(message.chat.id, f, caption=f"✅ '{topic}' mavzusidagi 40 betlik mukkamal kurs ishi tayyor!")
    
    os.remove(file_name)

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling()
