import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters
import yt_dlp
import instaloader
import threading
import requests

# Setup logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'YOUR_TOKEN' with your actual bot token
BOT_TOKEN = '7299908856:AAHdGphkZaCWc_e6NSWj9VYbi5lZ_MflKVg'

# Create directories for downloads
if not os.path.exists('downloads'):
    os.makedirs('downloads')

async def start(update: Update, context):
    welcome_message = (
        "Welcome to the Media Downloader Bot!\n"
        "Choose a platform by typing one of the following commands:\n"
        "/youtube - Download YouTube videos\n"
        "/facebook - Download Facebook videos\n"
        "/instagram - Download Instagram posts\n"
        "/twitter - Download Twitter videos\n"
    )
    await update.message.reply_text(welcome_message)

async def youtube(update: Update, context):
    await update.message.reply_text("Please send the YouTube link you want to download.")

async def facebook(update: Update, context):
    await update.message.reply_text("Please send the Facebook link you want to download.")

async def instagram(update: Update, context):
    await update.message.reply_text("Please send the Instagram link you want to download.")

async def twitter(update: Update, context):
    await update.message.reply_text("Please send the Twitter link you want to download.")

async def download_media(update: Update, context):
    link = update.message.text
    try:
        if "youtube.com" in link or "youtu.be" in link:
            await download_youtube(update, context, link)
        elif "facebook.com" in link:
            await download_facebook(update, context, link)
        elif "instagram.com" in link:
            await download_instagram(update, context, link)
        elif "twitter.com" in link:
            await download_twitter(update, context, link)
        else:
            await update.message.reply_text("Unsupported link. Please provide a valid link from YouTube, Facebook, Instagram, or Twitter.")
    except Exception as e:
        logger.error(f"Error occurred: {str(e)}", exc_info=True)
        await update.message.reply_text(f"An error occurred: {str(e)}")

async def download_youtube(update, context, link):
    await update.message.reply_text("Downloading your YouTube video, please wait...")
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best'  # This tries to select the best quality video
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            
            # Check available formats
            formats = info_dict.get('formats', [])
            if not formats:
                await update.message.reply_text("No formats available for this video.")
                return
            
            # Optional: Print available formats for debugging
            format_list = "\n".join(
                [f"{fmt.get('format_id', 'unknown_id')}: {fmt.get('format_note', 'N/A')} - {fmt.get('ext', 'unknown_ext')}" for fmt in formats]
            )
            logger.info(f"Available formats:\n{format_list}")
            
            # Set preferred format (e.g., 'best' or a specific format id)
            best_format = 'best'
            ydl_opts['format'] = best_format

            # Download the video with the selected format
            ydl = yt_dlp.YoutubeDL(ydl_opts)
            info_dict = ydl.extract_info(link, download=True)
            video_file = ydl.prepare_filename(info_dict)
        
        await send_file(update, context, video_file)
    except Exception as e:
        logger.error(f"Error downloading YouTube video: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error downloading YouTube video: {str(e)}")

async def download_instagram(update, context, link):
    await update.message.reply_text("Downloading your Instagram post, please wait...")
    L = instaloader.Instaloader(dirname_pattern='downloads')
    try:
        post = instaloader.Post.from_shortcode(L.context, link.split("/")[-2])
        L.download_post(post, target="downloads")
        media_files = [f for f in os.listdir('downloads') if f.endswith(('.jpg', '.mp4'))]
        for media_file in media_files:
            await send_file(update, context, f'downloads/{media_file}')
    except Exception as e:
        logger.error(f"Error downloading Instagram post: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error downloading Instagram post: {str(e)}")

async def download_facebook(update, context, link):
    await update.message.reply_text("Downloading your Facebook video, please wait...")
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': 'best'
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)
            media_file = ydl.prepare_filename(info_dict)
        await send_file(update, context, media_file)
    except Exception as e:
        logger.error(f"Error downloading Facebook video: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error downloading Facebook video: {str(e)}")

async def download_twitter(update, context, link):
    await update.message.reply_text("Downloading your Twitter video, please wait...")
    await update.message.reply_text("Twitter download feature is under construction.")

async def send_file(update, context, file_path):
    try:
        await context.bot.send_document(chat_id=update.effective_chat.id, document=open(file_path, 'rb'))
        os.remove(file_path)
    except Exception as e:
        logger.error(f"Error sending file: {str(e)}", exc_info=True)
        await update.message.reply_text(f"Error sending file: {str(e)}")

if __name__ == '__main__':
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('youtube', youtube))
    application.add_handler(CommandHandler('facebook', facebook))
    application.add_handler(CommandHandler('instagram', instagram))
    application.add_handler(CommandHandler('twitter', twitter))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_media))

    application.run_polling(poll_interval=3)
