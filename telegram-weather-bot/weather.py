import requests
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler, MessageHandler, filters

from config import TELEGRAM_API_KEY, WEATHER_API_KEY

logging.basicConfig(format='%(asctime)s - %(name) - %(levelname) - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Getting weather information from the weather API

async def get_weather(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)

    data = response.json()
    

    if data['cod'] == 200:
        weather_description = data['weather'][0]['description']
        temperature = data['main']['temp']
        feels_like = data['main']['feels_like']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']

        weather_info = (f"🌆 Weather in {city.capitalize()} 🌆\n\n"
                        f"🌤️ Description: {weather_description}\n"
                        f"🌡️ Temperature: {temperature}°C\n"
                        f"🧥 Feels Like: {feels_like}°C\n"
                        f"💧 Humidity: {humidity}%\n"
                        f"🌬️ Wind Speed: {wind_speed} m/s"
                        )
        return weather_info
    else:
        return "City not found. Please check the city name for error"
    
# Bot Commands

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Keyboard Inline Commands

    keyboard = [
        [InlineKeyboardButton('Set Location', callback_data='set_location')],
        [InlineKeyboardButton('London Weather', callback_data='weather_London')],
        [InlineKeyboardButton('New York Weather', callback_data='weather_New York')],
        [InlineKeyboardButton('Help', callback_data='help')],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
    "🌟 Hello! I'm your Weather Bot 🌟\n"
    "🌦️ Welcome to Weather Bot! Your go-to assistant for real-time weather updates.\n\n"
    "📍 Features:\n\n"
    "   • Get Weather Updates: Easily retrieve weather info for any city with the /weather command.\n"
    "   • Predefined City Weather: Check weather for cities like London and New York with a click.\n"
    "   • Interactive Inline Keyboard: Use buttons to get instant updates or query specific cities.\n\n"
    "💡 How to Use:\n\n"
    "   • Start the Bot: Use the /start command to access the main menu.\n"
    "   • Weather for Cities: Click buttons for predefined cities or use /weather [city] for custom queries.\n"
    "🌟 Stay informed and plan your day with accurate weather info at your fingertips!"
    , reply_markup=reply_markup)
    

# Button Function

async def button(update: Update, context: ContextTypes):
    query = update.callback_query
    await query.answer()

    if query.data.startswith('weather_'):
        city = query.data.split('_')[1]

        weather_info = await get_weather(city)
        await query.message.reply_text(text=weather_info)
    elif query.data == 'set_location':
        await query.message.reply_text(text='Please send your location with the /weather command.')
    elif query.data == 'help':
        await query.message.reply_text(text="Use /weather to get a specific location's weather")


# Weather Function

async def weather(update: Update, context: ContextTypes):
    if context.args:
        city = ' '.join(context.args)
        weather_info = await get_weather(city)
        await update.message.reply_text(weather_info)
    else:
        await update.message.reply_text("Please provide a city name after the /weather command.")

if __name__ == '__main__':
    application = Application.builder().token(TELEGRAM_API_KEY).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('weather', weather))
    application.add_handler(CallbackQueryHandler(button))

    application.run_polling(poll_interval=3)