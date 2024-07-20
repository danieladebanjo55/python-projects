# sniper_bot.py
import time
from pumpfun_api import get_new_tokens, buy_token, sell_token
from telegram_bot import bot
from telegram import Bot
from config import TELEGRAM_API_KEY

bot = Bot(TELEGRAM_API_KEY)

def snipe_tokens():
    while True:
        tokens = get_new_tokens()
        for token in tokens:
            if filter_token(token):
                buy_response = buy_token(token['id'], 100)
                bot.send_message(chat_id='your_telegram_chat_id', text=f"Bought token: {token['name']}")
                time.sleep(10)  # Wait for some time before selling
                sell_response = sell_token(token['id'], 100)
                bot.send_message(chat_id='your_telegram_chat_id', text=f"Sold token: {token['name']} for profit")
        time.sleep(60)  # Check for new tokens every minute

def filter_token(token):
    # Apply filters such as 'has socials', 'reply/comment count', 'creator wallet'
    if token['socials'] and token['reply_count'] > 10 and token['creator_wallet'] == 'specific_wallet':
        return True
    return False

if __name__ == '__main__':
    snipe_tokens()