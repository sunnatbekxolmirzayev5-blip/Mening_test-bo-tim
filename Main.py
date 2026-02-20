
import telebot

# BotFather'dan olgan tokeningizni mana shu qo'shtirnoq ichiga yopishtiring
API_TOKEN = '8041216411:AAHfLKlXQ6ltm4Gtn2MAiwMTw-nBp71hmbg'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Bot ishga tushdi.")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

bot.infinity_polling()

