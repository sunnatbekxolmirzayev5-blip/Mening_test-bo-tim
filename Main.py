import telebot
from telebot import types

API_TOKEN = '8041216411:AAHfLKlXQ6ltm4Gtn2MAiwMTw-nBp71hmbg'
PAYMENT_TOKEN ='371317599:TEST:1771648533486' 

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("💳 Kurs ishi (5,000 so'm)")
    item2 = types.KeyboardButton("📞 Admin")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, "Xush kelibsiz! Kurs ishi endi juda arzon.", reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "💳 Kurs ishi (5,000 so'm)")
def send_invoice(message):
    bot.send_invoice(
        message.chat.id, 
        title="Arzon Kurs Ishi",
        description="Barcha uchun hamyonbop kurs ishi (Word)",
        provider_token=PAYMENT_TOKEN,
        currency="UZS",
        prices=[types.LabeledPrice(label="Kurs ishi", amount=500000)], # 5,000 so'm
        start_parameter="kurs-ishi-arzon",
        payload="test-payment"
    )

@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, "To'lov uchun rahmat! Kurs ishi xaridingiz tasdiqlandi. ✅")

bot.infinity_polling()



