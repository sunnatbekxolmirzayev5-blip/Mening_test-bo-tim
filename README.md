import telebot

# Tokeningizni shu yerga yozing
API_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"

bot = telebot.TeleBot(API_TOKEN)

# /start komandasi
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Salom! Men oddiy botman 🤖")

# Oddiy matnli javoblar
@bot.message_handler(func=lambda message: True)
def echo(message):
    if message.text.lower() == "salom":
        bot.reply_to(message, "Salom 👋")
    elif message.text.lower() == "yaxshimisiz":
        bot.reply_to(message, "Ha, rahmat 😊")
    else:
        bot.reply_to(message, "Men hali oddiy botman 😅")

print("Bot ishga tushdi...")
bot.polling()