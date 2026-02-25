import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
import google.generativeai as genai

# --- TOKENLAR ---
TOKEN = "BOT_TOKEN"
GEMINI_KEY = "GEMINI_API_KEY"

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()


# --- HOLATLAR ---
class IshForm(StatesGroup):
    mavzu = State()
    til = State()
    list_soni = State()


# --- START ---
@dp.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(IshForm.mavzu)
    await message.answer("📚 Mustaqil ish mavzusini kiriting:")


# --- MAVZU ---
@dp.message(IshForm.mavzu)
async def get_mavzu(message: Message, state: FSMContext):
    await state.update_data(mavzu=message.text)
    await state.set_state(IshForm.til)
    await message.answer("🌍 Tilni tanlang (uz / ru / en):")


# --- TIL ---
@dp.message(IshForm.til)
async def get_til(message: Message, state: FSMContext):
    await state.update_data(til=message.text.lower())
    await state.set_state(IshForm.list_soni)
    await message.answer("📄 Necha bet (list) bo‘lsin? (masalan: 5)")


# --- LIST SONI ---
@dp.message(IshForm.list_soni)
async def generate_work(message: Message, state: FSMContext):
    data = await state.get_data()
    mavzu = data["mavzu"]
    til = data["til"]
    list_soni = message.text

    await message.answer("⏳ Ish tayyorlanmoqda...")

    prompt = f"""
    {til} tilida {list_soni} betlik mustaqil ish yoz.
    Mavzu: {mavzu}
    Reja, kirish, asosiy qism, xulosa va foydalanilgan adabiyotlar bo‘lsin.
    """

    response = model.generate_content(prompt)
    text = response.text

    file_name = f"{mavzu}.pdf"
    doc = SimpleDocTemplate(file_name)
    elements = []

    styles = getSampleStyleSheet()

    pdfmetrics.registerFont(UnicodeCIDFont('HYSMyeongJo-Medium'))

    custom_style = ParagraphStyle(
        'Custom',
        parent=styles['Normal'],
        fontName='HYSMyeongJo-Medium',
        fontSize=12,
        leading=16
    )

    for line in text.split("\n"):
        elements.append(Paragraph(line, custom_style))
        elements.append(Spacer(1, 0.2 * inch))

    doc.build(elements)

    await message.answer_document(FSInputFile(file_name))
    os.remove(file_name)

    await state.clear()


# --- ISHGA TUSHIRISH ---
async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    print("Bot ishga tushdi!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())