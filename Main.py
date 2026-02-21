import telebot
from telebot import types
import time
import os

# --- SOZLAMALAR ---
API_TOKEN = os.getenv("8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg")      # Tokenni environmentdan oling
PAYMENT_TOKEN = os.getenv("398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065")
ADMIN_ID =8016405262 

bot = telebot.TeleBot(API_TOKEN)

# Eski webhookni o‘chirish (409 xato uchun)
bot.remove_webhook()
time.sleep(1)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📝 Kurs ishi buyurtma berish"))
    bot.send_message(message.chat.id, "Bot ishga tushdi ✅", reply_markup=markup)

@bot.message_handler(func=lambda m: m.text == "📝 Kurs ishi buyurtma berish")
def get_topic(message):
    sent = bot.send_message(message.chat.id, "Mavzuni kiriting:")
    bot.register_next_step_handler(sent, send_payment)

def send_payment(message):
    user_topic = message.text

    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 5,000 so'm to'lash", callback_data=f"buy|{user_topic}"))

    bot.send_message(
        message.chat.id,
        f"📚 Mavzu: {user_topic}\n\nTo'lov qilish uchun tugmani bosing:",
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: call.data.startswith("buy"))
def pay(call):
    topic = call.data.split("|")[1]

    prices = [types.LabeledPrice(label="Kurs ishi", amount=500000)]  # 5000 so‘m = 500000 tiyin

    bot.send_invoice(
        chat_id=call.message.chat.id,
        title="Kurs ishi buyurtma",
        description=f"Mavzu: {topic}",
        provider_token=PAYMENT_TOKEN,
        currency="UZS",
        prices=prices,
        payload="order_info"
    )

@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, "✅ To'lov muvaffaqiyatli! Fayl tez orada yuboriladi.")
    bot.send_message(ADMIN_ID, f"🆕 Yangi buyurtma!\nUser: {message.from_user.id}")

if __name__ == "__main__":
    print("Bot ishga tushdi...")
    bot.infinity_polling(skip_pending=True, timeout=60, long_polling_timeout=60)
