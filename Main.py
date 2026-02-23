import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.chat_action import ChatActionSender
import google.generativeai as genai

# --- SOZLAMALAR ---
TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"
GEMINI_KEY = "AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw"

# Gemini AI sozlash
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# Logging
logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- HANDLERLAR ---

@dp.message(CommandStart())
async def start_cmd(message: Message):
    await message.answer(
        f"Salom {message.from_user.first_name}! 🌟\n"
        "Men Gemini AI bilan ishlovchi aqlli botman.\n"
        "Savolingizni bemalol yozishingiz mumkin."
    )

@dp.message(F.text)
async def chat_with_ai(message: Message):
    # Bot yozayotganini ko'rsatish
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        try:
            # AI dan javob olish
            response = model.generate_content(message.text)
            
            if response.text:
                # Markdown belgilari bilan yuborish
                await message.answer(response.text, parse_mode="Markdown")
            else:
                await message.answer("Kechirasiz, javob bera olmadim.")
        
        except Exception as e:
            logging.error(f"Xatolik: {e}")
            # Agar Markdown xatosi bo'lsa, oddiy matn yuborish
            try:
                await message.answer(response.text)
            except:
                await message.answer("⚠️ Hozircha javob berishda muammo bor.")

# --- ISHGA TUSHIRISH (CONFLICTSIZ) ---
async def main():
    # Botni ishga tushirishdan oldin eski webhook yoki sessiyalarni o'chirish
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot muvaffaqiyatli ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("To'xtatildi")


