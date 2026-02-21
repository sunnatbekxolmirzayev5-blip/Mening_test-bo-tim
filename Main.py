import telebot
import google.generativeai as genai

# API kalitlarini o'zgartiring!
TELEGRAM_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg "
GEMINI_API_KEY = "AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw"

# Gemini API-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# Telegram botni ishga tushirish
bot = telebot.TeleBot(TELEGRAM_TOKEN)

# /start komandasiga javob
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men Gemini bilan ishlaydigan Telegram botman.")

# Har qanday matnga javob berish
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    try:
        # Gemini-dan javob olish
        response = model.generate_content(message.text)
        bot.reply_to(message, response.text)
    except Exception as e:
        bot.reply_to(message, "Kechirasiz, xatolik yuz berdi: " + str(e))

# Botni doimiy ravishda ishlatish
bot.infinity_polling()
