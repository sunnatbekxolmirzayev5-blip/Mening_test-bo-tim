import os
import random
import google.generativeai as genai
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# --- SOZLAMALAR ---
TELEGRAM_TOKEN = "8041216411:AAGvwsCzDNlJNbKCXq8gpjWy8rkAZz5hqyg"
GEMINI_API_KEY = "AIzaSyBE67Ted_BbPRsWKcDeOnrzzSoV3T_IjLw"

# Gemini AI ni sozlash
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# 40 ta ma'lumot generatsiya qilish funksiyasi
def get_40_list():
    ismlar = ["Ali", "Vali", "Gani", "Sardor", "Malika", "Zilola", "Jasur", "Otabek", "Madina", "Nodira"]
    data = [f"{i}. {random.choice(ismlar)} - Natija: {random.randint(50, 100)}%" for i in range(1, 41)]
    return "\n".join(data)

# /start komandasi uchun funksiya
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    list_40 = get_40_list()
    await update.message.reply_text(f"Assalomu alaykum! Mana 40 ta ma'lumot:\n\n{list_40}")
    await update.message.reply_text("Endi menga ixtiyoriy savol bering, Gemini AI javob beradi!")

# Gemini AI bilan muloqot funksiyasi
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Xatolik yuz berdi. API kalitni tekshiring.")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot ishga tushdi...")
    app.run_polling()

if __name__ == "__main__":
    main()
