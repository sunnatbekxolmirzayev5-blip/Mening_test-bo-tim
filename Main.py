import telebot

# BotFather'dan olgan tokeningizni ' ' belgilari orasiga qo'ying
API_TOKEN = '8234527643:AAG3ldC-MD4dYyZUfoOnUHcqACZDjeo2c94'

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Salom! Men GitHub-ga yuklangan botman.")

bot.polling()
