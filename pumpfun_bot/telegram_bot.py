from telegram import Bot, Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import requests
from config import TELEGRAM_API_KEY, SOLANA_ADDRESS
from pump_api import buy_token, sell_token

# Helper function to get Solana price
def get_solana_price():
    response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=solana&vs_currencies=usd')
    data = response.json()
    return data['solana']['usd']

# Commands
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    sol_price = get_solana_price()
    message = (f"Hello {user.first_name}! Welcome to Hippie Sniper Bot V4.2.1 🚀\n\n"
               f"You currently have: 0 SOL\n\n"
               f"Your referral points: 0 points\n\n"
               "⚡️ Buy on PumpFun, Sell on Raydium 💰\n\n"
               "To get started trading, you can open a position by buying a token.\n\n"
               "🚀 To buy a token, just paste a token address or paste a Pump.fun URL or Dexscreener.com, "
               "and you will see a Buy dashboard pop up where you can choose how much you want to buy. "
               "Don't hesitate to use Fast Trading in Settings to trade more quickly.\n"
               "Use /start to see this menu again\n"
               f"{SOLANA_ADDRESS} (Tap to copy)\n\n"
               f"Current SOL Price: {sol_price}")

    buttons = [['🅱️BUY', '🤑SELL', '💵POSITIONS'], ['🪙LIMIT ORDER', '💰WITHDRAW', '🆘HELP']]
    reply_markup = ReplyKeyboardMarkup(buttons, resize_keyboard=True)

    await update.message.reply_text(message, reply_markup=reply_markup)

async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please enter the token address or Pump.fun URL:")

async def sell(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please enter the token address or Pump.fun URL:")

async def positions(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Here are your current positions:")

async def limit_order(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please enter the details for the limit order:")

async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Please enter the Solana address to withdraw your funds:")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Help information and commands here.")

async def handle_token_buy(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    token_address = update.message.text
    response = buy_token(token_address, amount=100)  # You can customize the amount or get it from the user
    await update.message.reply_text(f"Successfully bought token: {token_address}")

def main():
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^BUY$'), buy))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^SELL$'), sell))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^POSITIONS$'), positions))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^LIMIT ORDER$'), limit_order))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^WITHDRAW$'), withdraw))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex('^HELP$'), help_command))
    application.add_handler(MessageHandler(filters.TEXT, handle_token_buy))

    application.run_polling()

if __name__ == '__main__':
    main()