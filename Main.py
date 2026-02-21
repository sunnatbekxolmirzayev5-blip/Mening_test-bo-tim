import telebot
from telebot import types

# 1. SOZLAMALAR
API_TOKEN = '8041216411:AAHfLKlXQ6ltm4Gtn2MAiwMTw-nBp71hmbg'
PAYMENT_TOKEN = '371317599:TEST:1771648533486' 
ADMIN_ID = 8016405262 # O'z ID raqamingizni kiriting

bot = telebot.TeleBot(API_TOKEN)

# Foydalanuvchi ma'lumotlarini vaqtinchalik saqlash
user_data = {}

# 2. START BUYRUG'I
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("📝 Kurs ishi yaratish")
    item2 = types.KeyboardButton("📞 Admin")
    markup.add(item1, item2)
    
    bot.send_message(
        message.chat.id, 
        f"Salom {message.from_user.first_name}! 👋\nMen kurs ishingizni yaratishga yordam beraman. Boshlash uchun tugmani bosing.", 
        reply_markup=markup
    )

# 3. KURS ISHI YARATISH BOSQICHLARI
@bot.message_handler(func=lambda message: message.text == "📝 Kurs ishi yaratish")
def ask_topic(message):
    msg = bot.send_message(message.chat.id, "Kurs ishingiz mavzusini kiriting (Masalan: Sun'iy intellekt):")
    bot.register_next_step_handler(msg, process_topic)

def process_topic(message):
    topic = message.text
    user_data[message.chat.id] = {'topic': topic}
    
    # Avtomatik reja namunasi
    reja = (
        f"✅ **'{topic}' mavzusi bo'yicha reja tayyor:**\n\n"
        "1. Kirish\n"
        f"2. {topic}ning nazariy asoslari\n"
        f"3. O'zbekistonda {topic} tahlili\n"
        "4. Xulosa va takliflar\n\n"
        "💰 Ushbu kurs ishini to'liq (Word) yuklab olish narxi: 5,000 so'm."
    )
    
    markup = types.InlineKeyboardMarkup()
    pay_button = types.InlineKeyboardButton(text="💳 To'lov qilish va yuklab olish", callback_data="buy_now")
    markup.add(pay_button)
    
    bot.send_message(message.chat.id, reja, reply_markup=markup, parse_mode="Markdown")

# 4. TO'LOV JARAYONI (CALLBACK)
@bot.callback_query_handler(func=lambda call: call.data == "buy_now")
def handle_payment(call):
    topic = user_data.get(call.message.chat.id, {}).get('topic', 'Kurs ishi')
    
    bot.send_invoice(
        call.message.chat.id, 
        title=f"{topic} (Kurs ishi)",
        description="To'liq tayyorlangan kurs ishi paketi",
        provider_token=PAYMENT_TOKEN,
        currency="UZS",
        prices=[types.LabeledPrice(label="Kurs ishi", amount=500000)], # 5,000 so'm
        start_parameter="kurs-ishi-gen",
        payload="payment-success"
    )

# 5. TO'LOVNI TASDIQLASH
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    topic = user_data.get(message.chat.id, {}).get('topic', 'Kurs ishi')
    bot.send_message(message.chat.id, f"✅ To'lov qabul qilindi! '{topic}' mavzusidagi kurs ishi 5 daqiqa ichida yuboriladi.")
    
    # Adminga xabar
    bot.send_message(ADMIN_ID, f"💰 Pul tushdi!\nMavzu: {topic}\nFoydalanuvchi: @{message.from_user.username}")

bot.infinity_polling()


