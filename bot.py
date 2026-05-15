import os
import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
import google.generativeai as genai

# Configuración para que corra en Render sin problemas
nest_asyncio.apply()

# --- TUS DATOS REALES ---
TOKEN_TELEGRAM = "8294425780:AAFsJneyGPeLo35arLH2Hv5oaBeCy9iOxDw"
API_KEY_GEMINI = "AIzaSyBWnKkz7crtzxjYqqhHtlX_RNIO_7kZNsA"

# Configurar Gemini
genai.configure(api_key=API_KEY_GEMINI)
model = genai.GenerativeModel('gemini-pro')

async def responder(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    print(f"Mensaje recibido: {user_message}")
    
    try:
        # Generar respuesta con la IA de Google
        response = model.generate_content(user_message)
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("Mano, hubo un error con Gemini. Intenta de nuevo.")

async def main():
    print("🤖 BOT ONLINE EN RENDER")
    app = ApplicationBuilder().token(TOKEN_TELEGRAM).build()
    
    # Manejador de mensajes
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), responder))
    
    # Iniciar procesos
    await app.initialize()
    await app.start()
    await app.updater.start_polling()
    
    # Mantener el bot encendido
    while True:
        await asyncio.sleep(1)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
