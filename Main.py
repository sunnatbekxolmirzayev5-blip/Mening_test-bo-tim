import telebot
from telebot import types
import time

# Sizning bot tokeningiz
TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📚 Mukkamal Kurs ishi yozish"))
    bot.send_message(message.chat.id, f"Assalomu alaykum, {message.from_user.first_name}! 👋\nMavzu yozsangiz, men uni 12 varaqqa yetadigan qilib yozib beraman.", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📚 Mukkamal Kurs ishi yozish")
def ask_topic(message):
    msg = bot.send_message(message.chat.id, "Kurs ishi mavzusini kiriting:")
    bot.register_next_step_handler(msg, generate_work)

def generate_work(message):
    topic = message.text
    bot.send_message(message.chat.id, "⏳ Reja asosida mukkamal matn tayyorlanmoqda... (10 soniya kuting)")
    
    # 1. REJA
    reja = (f"📋 **'{topic}' mavzusida kurs ishi REJASI:**\n\n"
            "KIRISH (Mavzuning dolzarbligi)\n"
            "I-BOB. Nazariy va uslubiy asoslar\n"
            "   1.1. Atamalarning kelib chiqishi\n"
            "   1.2. Sohaning tarixiy rivojlanishi\n"
            "II-BOB. Amaliy tahlil va statistik ma'lumotlar\n"
            "   2.1. Mavjud holat tahlili\n"
            "   2.2. Muammolar va ularning yechimlari\n"
            "XULOSA VA TAKLIFLAR\n"
            "FOYDALANILGAN ADABIYOTLAR")

    # 2. MATN (Daftarni to'ldirish uchun kengaytirilgan)
    matn = (f"📘 **KIRISH VA ASOSIY QISM**\n\n"
            f"{topic} bugungi kunda jamiyatning eng dolzarb masalalaridan biri hisoblanadi. "
            f"Ushbu sohani o'rganish jarayonida biz shuni aniqladikki, {topic} tizimi "
            "nafaqat texnik, balki ijtimoiy-iqtisodiy jihatdan ham katta ahamiyatga ega. "
            "Daftarning dastlabki 6 betini to'ldirish uchun har bir bandga o'z fikringizni qo'shib, "
            "misollar bilan boyitib yozing. Masalan, ushbu sohaning O'zbekistondagi o'rni haqida to'xtaling...")

    xulosa = (f"📑 **II-BOB VA XULOSA**\n\n"
              f"Tahlillar shuni ko'rsatadiki, {topic} bo'yicha amaliyotda bir qancha kamchiliklar bor. "
              "Buni bartaraf etish uchun innovatsion usullardan foydalanish shart. Xulosa qilib aytganda, "
              "bu mavzu kelajakda yanada ko'proq tadqiqotlarni talab qiladi. "
              "Ushbu matnlar yordamida daftarning qolgan 6 betini bemalol to'ldira olasiz.")

    bot.send_message(message.chat.id, reja, parse_mode="Markdown")
    time.sleep(3)
    bot.send_message(message.chat.id, matn, parse_mode="Markdown")
    time.sleep(3)
    bot.send_message(message.chat.id, xulosa, parse_mode="Markdown")
    bot.send_message(message.chat.id, "✅ Tayyor! 12 varaqni to'ldirish uchun ushbu qismlarni kengaytirib yozing.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.infinity_polling(skip_pending=True)
