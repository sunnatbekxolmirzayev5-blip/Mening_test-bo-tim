

    import asyncio
import logging
import google.generativeai as genai
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# --- SOZLAMALAR ---
TELEGRAM_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"
GEMINI_API_KEY = "AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw"

# Gemini-ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Bot va Dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# /start komandasi uchun handler
@dp.message(CommandStart())
async def start_handler(message: types.Message):
    await message.answer("Salom! Men Gemini AI bilan ulangan botman. Savolingizni bering!")

# Xabarlarni qabul qilib, Gemini-ga yuborish
@dp.message()
async def chat_handler(message: types.Message):
    # Bot "yozmoqda..." holatida ko'rinishi uchun
    await bot.send_chat_action(message.chat.id, "typing")
    
    try:
        # Gemini-dan javob olish
        response = model.generate_content(message.text)
        
        # Javobni Telegramga yuborish
        await message.answer(response.text)
    except Exception as e:
        logging.error(f"Xatolik yuz berdi: {e}")
        await message.answer("Kechirasiz, javob qaytarishda xatolik yuz berdi.")

# Botni ishga tushirish
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot to'xtatildi")
