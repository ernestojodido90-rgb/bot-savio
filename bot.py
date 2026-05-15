import os
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Configuración necesaria para entornos como Render o Colab
nest_asyncio.apply()

# --- CONFIGURACIÓN DE APIS ---
# Reemplaza con tus llaves reales entre las comillas
TOKEN_TELEGRAM = "TU_TOKEN_DE_TELEGRAM_AQUÍ"
API_KEY_GEMINI = "TU_API_KEY_DE_GEMINI_AQUÍ"

# Configurar Gemini
genai.configure(api_key=API_KEY_GEMINI)
model = genai.GenerativeModel('gemini-pro')

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"Mensaje recibido: {user_message}")
    
    try:
        # Generar respuesta con la IA
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Mano, tuve un error con la IA. Intenta de nuevo.")

async def main():
    print("🤖 BOT ONLINE - Escríbeme en Telegram")
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()
    
    # Manejador de mensajes de texto
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    
    # Iniciar el bot
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Mantener el bot corriendo
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
