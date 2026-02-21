import telebot
from telebot import types
import time

# BotFather dan olgan API tokeningiz
API_TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg' 

bot = telebot.TeleBot(API_TOKEN)

# 1. START BUYRUG'I
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📚 Kurs ishi / Slayt yaratish"))
    
    bot.send_message(
        message.chat.id, 
        f"Salom {message.from_user.first_name}! 👋\nMavzu yozing, men reja tuzib beraman.", 
        reply_markup=markup
    )

# 2. MAVZUNI QABUL QILISH
@bot.message_handler(func=lambda m: m.text == "📚 Kurs ishi / Slayt yaratish")
def ask_topic(message):
    msg = bot.send_message(message.chat.id, "Mavzuni yozib yuboring:")
    bot.register_next_step_handler(msg, send_result)

# 3. NATIJANI CHIQARISH
def send_result(message):
    topic = message.text
    javob = (
        f"✅ **'{topic}'** mavzusi bo'yicha reja:\n\n"
        "1. Kirish (Mavzu mohiyati)\n"
        "2. Asosiy qism (Nazariy tahlil)\n"
        "3. Amaliy bo'lim (Statistika)\n"
        "4. Xulosa va foydalanilgan adabiyotlar.\n\n"
        "✍️ Ushbu reja asosida kurs ishingizni tayyorlashingiz mumkin."
    )
    bot.send_message(message.chat.id, javob, parse_mode="Markdown")

# 4. BOTNI ISHGA TUSHIRISH (XATOLARNI OLDINI OLISH)
if __name__ == "__main__":
    try:
        bot.remove_webhook() # Eski ulanishlarni uzish
        time.sleep(1)
        print("Bot ishlamoqda...")
        bot.infinity_polling(skip_pending=True)
    except Exception as e:
        print(f"Xatolik: {e}")

