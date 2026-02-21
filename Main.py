import telebot
from telebot import types

API_TOKEN = '8041216411:AAHfLKlXQ6ltm4Gtn2MAiwMTw-nBp71hmbg'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    # Tugmalarni yaratish
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📚 Mavzularni ko'rish")
    item2 = types.KeyboardButton("📝 Kurs ishi tartibi")
    item3 = types.KeyboardButton("📞 Bog'lanish")
    
    markup.add(item1, item2, item3)
    
    bot.send_message(message.chat.id, "Salom! Kurs ishi botiga xush kelibsiz. Quyidagi menyudan birini tanlang:", reply_markup=markup)

@bot.message_handler(func=lambda message: True)
def handle_text(message):
    if message.text == "📚 Mavzularni ko'rish":
        bot.send_message(message.chat.id, "Mavjud mavzular:\n1. Sun'iy intellekt\n2. Kiberxavfsizlik\n3. Ma'lumotlar bazasi")
    
    elif message.text == "📝 Kurs ishi tartibi":
        bot.send_message(message.chat.id, "Kurs ishi 25-30 bet bo'lishi, mundarija va xulosaga ega bo'lishi kerak.")
    
    elif message.text == "📞 Bog'lanish":
        bot.send_message(message.chat.id, "Yordam uchun: @admin_username ga yozing.")
    
    else:
        bot.reply_to(message, "Tushunmadim, iltimos tugmalardan foydalaning.")

bot.infinity_polling()


