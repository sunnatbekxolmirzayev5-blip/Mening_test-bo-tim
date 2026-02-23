import asyncio
import logging
import sqlite3
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.chat_action import ChatActionSender

# --- SOZLAMALAR ---
# Tokenlarni bu yerga joylashtiring
TELEGRAM_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"
GEMINI_API_KEY = "AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw"

# Gemini AI sozlamalari
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Logging (Xatoliklarni kuzatish uchun)
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# --- MA'LUMOTLAR BAZASI ---
def init_db():
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            full_name TEXT,
            username TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_user(user_id, name, username):
    conn = sqlite3.connect("bot_data.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users VALUES (?, ?, ?)", (user_id, name, username))
    conn.commit()
    conn.close()

# --- TUGMALAR ---
def get_main_keyboard():
    buttons = [
        [KeyboardButton(text="🤖 AI haqida"), KeyboardButton(text="📊 Statistika")],
        [KeyboardButton(text="⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True)

# --- HANDLERLAR ---

@dp.message(CommandStart())
async def start_command(message: Message):
    save_user(message.from_user.id, message.from_user.full_name, message.from_user.username)
    
    welcome_text = (
        f"Assalomu alaykum, {message.from_user.first_name}!\n\n"
        "Men **Gemini AI** bilan kuchaytirilgan botman. "
        "Menga xohlagan savolingizni bering, men javob berishga harakat qilaman! 🚀"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard(), parse_mode="Markdown")

@dp.message(F.text == "📊 Statistika")
async def show_stats(message: Message):
    conn = sqlite3.connect("bot_data.db")
    count = conn.execute("SELECT COUNT(*) FROM users").fetchone()[0]
    conn.close()
    await message.answer(f"Botdan foydalanuvchilar soni: {count} ta")

@dp.message(F.text == "🤖 AI haqida")
async def about_ai(message: Message):
    await message.answer("Men Google tomonidan yaratilgan Gemini 1.5 Flash modeli asosida ishlayman. "
                         "Matn yozish, kod yozish va savollarga javob berishda juda tezman!")

# Gemini AI bilan muloqot qismi
@dp.message(F.text)
async def handle_ai_query(message: Message):
    # Foydalanuvchiga bot o'ylayotganini ko'rsatish
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        try:
            # Gemini-dan javob olish
            response = model.generate_content(message.text)
            
            # Agar javob bo'sh bo'lmasa, yuborish
            if response.text:
                # Telegramda 4096 belgidan ortiq xabar yuborib bo'lmaydi
                if len(response.text) > 4000:
                    for i in range(0, len(response.text), 4000):
                        await message.answer(response.text[i:i+4000])
                else:
                    await message.answer(response.text, parse_mode="Markdown")
            else:
                await message.answer("Kechirasiz, bu savolga javob topa olmadim.")
                
        except Exception as e:
            logging.error(f"Xatolik yuz berdi: {e}")
            await message.answer("⚠️ Hozirda AI xizmatida uzilish bor. Birozdan so'ng qayta urinib ko'ring.")

# --- ASOSIY FUNKSIYA ---
async def start():
    init_db()
    print("Bot muvaffaqiyatli ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start())

