import telebot
from telebot import types
import time

# 1. SOZLAMALAR
# Muhim: BotFather'dan yangi API token olgan bo'lsangiz, o'shani qo'ying
API_TOKEN = '8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg'
PAYMENT_TOKEN = '371317599:TEST:1771648533486' 
ADMIN_ID = 8016405262 # O'z ID raqamingiz

bot = telebot.TeleBot(API_TOKEN)

# 2. START BUYRUG'I
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("📝 Kurs ishi buyurtma qilish"))
    
    bot.send_message(
        message.chat.id, 
        f"Assalomu alaykum, {message.from_user.first_name}!\n"
        "Men sizga sifatli kurs ishi tayyorlab beraman.", 
        reply_markup=markup
    )

# 3. MAVZUNI SO'RASH VA REJA TUZISH
@bot.message_handler(func=lambda m: m.text == "📝 Kurs ishi buyurtma qilish")
def get_topic(message):
    sent = bot.send_message(message.chat.id, "Kurs ishi mavzusini yozib yuboring:")
    bot.register_next_step_handler(sent, send_reja)

def send_reja(message):
    topic = message.text
    reja_text = (
        f"✅ **'{topic}'** mavzusi qabul qilindi.\n\n"
        "📋 **Kurs ishi rejasi:**\n"
        "1. Kirish\n"
        "2. Nazariy qism (Tushunchalar)\n"
        "3. Amaliy tahlil va statistik ma'lumotlar\n"
        "4. Xulosa va takliflar\n\n"
        "💰 Narxi: 5,000 so'm"
    )
    
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("💳 To'lov qilish va yuklab olish", callback_data="pay"))
    bot.send_message(message.chat.id, reja_text, reply_markup=markup, parse_mode="Markdown")

# 4. TO'LOV INVOYSINI CHIQARISH (Karta kiritish joyi shunda chiqadi)
@bot.callback_query_handler(func=lambda call: call.data == "pay")
def create_invoice(call):
    bot.send_invoice(
        call.message.chat.id,
        title="Kurs ishi (Word)",
        description="Tayyor kurs ishi faylini yuklab olish uchun to'lov qiling.",
        provider_token=PAYMENT_TOKEN,
        currency="UZS",
        prices=[types.LabeledPrice(label="Kurs ishi", amount=500000)], # 5,000.00 UZS
        payload="order_id_123"
    )

# 5. TO'LOV JARAYONI (XAVFSIZLIK)
@bot.pre_checkout_query_handler(func=lambda q: True)
def checkout(q):
    bot.answer_pre_checkout_query(q.id, ok=True)

@bot.message_handler(content_types=['successful_payment'])
def success(message):
    bot.send_message(message.chat.id, "To'lov muvaffaqiyatli! ✅ Tez orada faylni yuboramiz.")
    # Adminga xabar
    bot.send_message(ADMIN_ID, f"💰 Yangi to'lov: 5,000 so'm\nUser: @{message.from_user.username}")

# 6. CONFLICT XATOSINI YO'QOTISH UCHUN ASOSIY QISM
if __name__ == "__main__":
    while True:
        try:
            bot.remove_webhook()
            print("Bot ishga tushmoqda...")
            bot.infinity_polling(skip_pending=True)
        except Exception as e:
            print(f"Xatolik yuz berdi: {e}")
            time.sleep(5) # Xato bo'lsa 5 soniya kutib qayta yoqiladi
