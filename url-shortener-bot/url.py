import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
import pyshorteners
import qrcode
from config import TELEGRAM_API_KEY
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
import io
import validators

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(message)s',
    level=logging.INFO
)

# Dictionary to store users' shortened links history and last shortened URL
user_history = {}
last_shortened_url = {}

# Start command
async def start(update: Update, context) -> None:
    await update.message.reply_text("Hi! Send me a URL, and I'll shorten it for you. You can also view your history with /history.")

# Shorten URL function
async def shorten_url(update: Update, context) -> None:
    user_message = update.message.text.strip()
    user_id = update.message.from_user.id

    # Validate the URL
    if validators.url(user_message):
        # Shorten the URL
        s = pyshorteners.Shortener()
        short_url = s.tinyurl.short(user_message)

        # Store the shortened URL in the user's history and last shortened URL
        if user_id not in user_history:
            user_history[user_id] = []
        user_history[user_id].append(short_url)
        last_shortened_url[user_id] = short_url

        # Create an inline keyboard for QR code generation
        keyboard = [
            [InlineKeyboardButton("Generate QR Code", callback_data="generate_qr")],
            [InlineKeyboardButton("View History", callback_data="view_history")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Send the shortened URL with the option to generate a QR code
        await update.message.reply_text(f"Here is your shortened URL: {short_url}", reply_markup=reply_markup)
    else:
        await update.message.reply_text("Please send a valid URL.")

# Callback query handler for QR code generation
async def generate_qr(update: Update, context) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    # Get the last shortened URL for the user
    short_url = last_shortened_url.get(user_id, None)
    if short_url:
        # Generate QR code
        qr_img = qrcode.make(short_url)
        qr_bytes = io.BytesIO()
        qr_img.save(qr_bytes)
        qr_bytes.seek(0)

        # Send the QR code image with a new keyboard to shorten another link
        keyboard = [
            [InlineKeyboardButton("Shorten Another Link", callback_data="shorten_another")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await query.message.reply_photo(photo=InputFile(qr_bytes), caption=f"Here is the QR code for your shortened URL.", reply_markup=reply_markup)
    else:
        await query.message.reply_text("Sorry, I couldn't find the last shortened URL.")

# Function to handle the "Shorten Another Link" button press
async def shorten_another(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    await query.message.reply_text("Send a new URL to shorten.")

# Function to handle the "View History" button press
async def view_history(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()

    if user_id in user_history and user_history[user_id]:
        history_text = "Here are your previously shortened links:\n" + "\n".join(user_history[user_id])
        await query.message.reply_text(history_text)
    else:
        await query.message.reply_text("You haven't shortened any URLs yet.")

# History command
async def history(update: Update, context) -> None:
    user_id = update.message.from_user.id

    if user_id in user_history and user_history[user_id]:
        history_text = "Here are your previously shortened links:\n" + "\n".join(user_history[user_id])
        await update.message.reply_text(history_text)
    else:
        await update.message.reply_text("You haven't shortened any URLs yet.")

if __name__ == '__main__':
    application = ApplicationBuilder().token(TELEGRAM_API_KEY).build()

    # Handlers for commands and messages
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('history', history))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, shorten_url))

    # Handlers for callback queries
    application.add_handler(CallbackQueryHandler(generate_qr, pattern="generate_qr"))
    application.add_handler(CallbackQueryHandler(shorten_another, pattern="shorten_another"))
    application.add_handler(CallbackQueryHandler(view_history, pattern="view_history"))

    # Start the bot
    application.run_polling(poll_interval=2)