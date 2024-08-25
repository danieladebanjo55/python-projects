from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from PIL import Image
import pytesseract
import io
import logging
import aiohttp
from config import TELEGRAM_API_KEY

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context):
    await update.message.reply_text('Send an image you want to extract text from.')

async def handle_image(update: Update, context):
    photo = update.message.photo[-1]
    file = await photo.get_file()
    file_url = file.file_path

    # Download the image using aiohttp
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            image_bytes = await response.read()

    # Use pytesseract to extract text
    image = Image.open(io.BytesIO(image_bytes))
    text = pytesseract.image_to_string(image)

    keyboard = [
            [InlineKeyboardButton("Extract New Text?", callback_data="new_image")]
        ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(f"Extracted text:\n{text}", reply_markup=reply_markup)

async def new_image(update: Update, context):
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Send me another image to extract the text...")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.PHOTO, handle_image))
    application.add_handler(CallbackQueryHandler(new_image, pattern='new_image'))

    application.run_polling(poll_interval=3)

