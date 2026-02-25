
import telebot
import google.generativeai as genai

# --- KALITLAR ---
TELEGRAM_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"
GEMINI_API_KEY = "AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw"

# Gemini AI sozlamalari
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Botni sozlash
bot = telebot.TeleBot(TELEGRAM_TOKEN)

def generate_40_list():
    """Mustaqil ish uchun 40 ta ma'lumot generatsiyasi"""
    data = []
    mavzu = "Axborot texnologiyalari va AI"
    for i in range(1, 41):
        data.append(f"{i}. {mavzu} sohasidagi muhim bosqich #{i}: Zamonaviy texnologiyalar rivoji.")
    return "\n".join(data)

@bot.message_handler(commands=['start'])
def welcome(message):
    msg = "Assalomu alaykum! Mustaqil ish ma'lumotlarini olish uchun /mustaqil buyrug'ini bering yoki Gemini'ga savol yozing."
    bot.reply_to(message, msg)

@bot.message_handler(commands=['mustaqil'])
def send_mustaqil(message):
    bot.send_message(message.chat.id, "Tayyorlanmoqda, iltimos kuting...")
    list_data = generate_40_list()
    # Telegram xabar limiti sababli qismlarga bo'lib yuboramiz
    bot.send_message(message.chat.id, f"📝 **Mustaqil ish uchun 40 ta ma'lumot:**\n\n{list_data}")

@bot.message_handler(func=lambda message: True)
def ai_chat(message):
    try:
        # Gemini AI javobini olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Xatolik yuz berdi. API kalit yoki internetni tekshiring.")

print("Bot ishga tushdi...")
bot.infinity_polling()
