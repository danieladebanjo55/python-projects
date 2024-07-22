import logging
import requests
from telegram import Update
from telegram.ext import Application, CallbackContext, CommandHandler, CallbackQueryHandler

from config import TELEGRAM_API_KEY, NEWS_API_KEY, NEWS_URL

# Setting Up Logger

logging.basicConfig(format='%(asctime)s - %(name) - %(levelname) - %(message)s', level=logging.INFO)
# logger = logging.getLogger(__name__)

# Commands

async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("Welcome to Hippie's Crypto News Bot! Use /news to get the latest crypto news updates.")

async def get_news(update: Update, context: CallbackContext) -> None:
    query = 'crypto'
    response = requests.get(NEWS_URL, params={
        'q': query,
        'apiKey': NEWS_API_KEY,
        'language': 'en',
        'sortBy': 'publishedAt',
    })
    data = response.json()

    if data['status'] == 'ok' and data['articles']:
        articles = data['articles'][:15]
        new_message = "Latest Cryto News:\n\n"
        # print(new_message)

        for article in articles:
            title = article['title']
            url = article['url']
            new_message += f"{title}\n{url}\n\n"

        # else:
        #     new_message = "No news found at the moment."

        await update.message.reply_text(new_message)

async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == 'refresh_news':
        await get_news(query, context)


# Main Function

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('news', get_news))

    application.run_polling(poll_interval=3)