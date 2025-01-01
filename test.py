import telebot
import requests
from bs4 import BeautifulSoup
from telebot import types
import os
import logging
import threading
import re
import time
import requests
from instaloader import Instaloader, Post
import logging
import yt_dlp
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from telebot import TeleBot, types

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Manually enter Telegram Bot Token and Spotify Credentials
TELEGRAM_TOKEN = "7723800476:AAH1pzcaD5POExu7SVWl7B3wmV-GVEVY0D8"

SPOTIPY_CLIENT_ID="c7e5aa9082a14ff898a1333022b83c4d"
SPOTIPY_CLIENT_SECRET="55683736338c4661b25cd40032d21f37"

# Instagram credentials
INSTAGRAM_USERNAME = "_renuka_1047"
INSTAGRAM_PASSWORD = "renu1047"



if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
    raise ValueError("Please set INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD in environment variables.")


if not TELEGRAM_TOKEN or not SPOTIPY_CLIENT_ID or not SPOTIPY_CLIENT_SECRET:
    raise ValueError("Please set TELEGRAM_BOT_TOKEN, SPOTIFY_CLIENT_ID, and SPOTIFY_CLIENT_SECRET in environment variables.")

bot = TeleBot(TELEGRAM_TOKEN)


@bot.message_handler(commands=['DETAILS'])
def send_details(message):
    details_text = (
        "🎉 DETAILED COMMANDS AND THEIR USAGE 🎉\n\n"
        "📺 1. /YOUTUBE <URL>\n"
        "   - 🎥 Download YouTube videos directly.\n"
        "   - 📝 *Example:* /YOUTUBE https://youtube.com/video-url\n"
        "   - 🔗 Provide a valid YouTube link to get started.\n\n"
        "🎵 2. /SPOTIFY <NAME OR URL>\n"
        "   - 🎶 Download songs from Spotify easily.\n"
        "   - 📝 *Example:* /SPOTIFY Song Name or /SPOTIFY https://spotify.com/song-url\n"
        "   - 🔍 Search by song name or paste the Spotify link.\n\n"
        "📸 3. JUST SEND THE <URL> IG LINK\n"
        "   - 📷 Download Instagram reels, stories, or posts.\n"
        "   - 📝 *Example:* https://instagram.com/post-url\n"
        "   - 🔗 Provide the Instagram post/reel/story link to download.\n\n"
        
        "👤 4. /MYINFO or /ID\n"
        "   - 🔍 View your Telegram profile details.\n"
        "   - 📄 Includes your username, Telegram ID, chat ID, last seen, and more.\n\n"
        "📜 5. /DETAILS\n"
        "   - 🛠️ Displays this detailed guide for all bot commands.\n"
        "   - 📖 Learn how to use the bot effectively.\n\n"
        "💡 TIPS & NOTES:\n"
        "   - ✅ Always provide valid links for commands like /YOUTUBE, /SPOTIFY, and YOU CAN /YOUTUBE FOR INSTAGRAM DOWNLOAD ALSO.\n"
        "   - 📵 Respect content policies for commands .\n"
        "   - 🚀 Enjoy the bot and explore its features responsibly!\n\n"
        "✨ THANK YOU FOR USING OUR BOT! ✨"
    )
    bot.send_message(message.chat.id, details_text)




# Command: /help
@bot.message_handler(commands=['help'])
def send_help(message):
    photo_url = "https://ibb.co/GvTvbgj"  # Replace with your image URL
    caption = (
        "HELLO THERE USAGE 👇\n"
        "/YOUTUBE <URL> = TO DOWNLOAD YOUTUBE VIDEOS\n"
        "/SPOTIFY <NAME OR URL> TO DOWNLOAD ANY SONGS\n"
        "/YOUTUBE = TO DOWNLOAD INSTAGRAM REELS, STORY, OR POST\n"
        "/MYINFO OR /ID = TO GET YOUR INFORMATION\n"
        "/DETAILS = TO SEE THE DETAILS\n\n"
        "THANK YOU FOR USING OUR BOT!"
    )
    bot.send_photo(chat_id=message.chat.id, photo=photo_url, caption=caption)

# Command: /myinfo or /id
@bot.message_handler(commands=['MYINFO', 'ID'])
def send_user_info(message):
    user = message.from_user

    # Fetch user details
    username = user.username or "N/A"
    tg_id = user.id
    chat_id = message.chat.id
    first_name = user.first_name or "N/A"
    last_name = user.last_name or "N/A"

    # Check if the user has a profile photo
    photos = bot.get_user_profile_photos(user.id)
    if photos.total_count > 0:
        photo_id = photos.photos[0][0].file_id
    else:
        photo_id = None

    caption = (
        f"TG USERNAME -> {username}\n"
        f"TG ID -> {tg_id}\n"
        f"CHAT ID -> {chat_id}\n"
        f"LAST SEEN -> {last_name}\n"
        f"USED THIS BOT -> {'Yes' if user.is_bot else 'No'}\n"
        f"PH NO. -> N/A"  # Telegram API doesn't provide phone numbers
    )

    # Send profile photo if available
    if photo_id:
        bot.send_photo(chat_id=message.chat.id, photo=photo_id, caption=caption)
    else:
        bot.send_message(chat_id=message.chat.id, text=caption)

@bot.message_handler(commands=['start'])
def start_command(message):
    # Photo link (use your own link for the bot photo)
    photo_link = "https://ibb.co/GvTvbgj"
    bot.send_photo(message.chat.id, photo_link)

    # Welcome message
    welcome_message = (
        "WELCOME TO THE EMPOWERDED CHANNEL! 🎉\n\n"
        "This bot can:\n"
        "- 📹 Download YouTube videos\n"
        "- 🎵 Play and download songs\n"
        "- 🎵 Play and download Instagram\n"
        "Type /help to see tutorial and usage instructions.\n\n"
        "Please choose one option below:"
    )
    
    # Add buttons for GitHub, Support, and Telegram Channel
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    github_button = types.KeyboardButton("GitHub")
    support_button = types.KeyboardButton("Support")
    telegram_button = types.KeyboardButton("Official Telegram Channel")
    
    markup.add(github_button, support_button, telegram_button)

    bot.reply_to(
        message,
        welcome_message,
        reply_markup=markup,
    )

# Handlers for the new buttons
@bot.message_handler(func=lambda message: message.text == "GitHub")
def send_github_link(message):
    bot.send_message(message.chat.id, "Check out my GitHub here: [GitHub Link](https://github.com/abhinai2244)", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Support")
def send_support_link(message):
    bot.send_message(message.chat.id, "Join our support Telegram group here: [Support Group](https://t.me/clutch008)", parse_mode="Markdown")

@bot.message_handler(func=lambda message: message.text == "Official Telegram Channel")
def send_telegram_channel_link(message):
    bot.send_message(message.chat.id, "Join our official Telegram channel here: [Official Channel](https://t.me/ARMANTEAMVIP)", parse_mode="Markdown")


   



# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET))

# yt-dlp options
YDL_OPTIONS = {
    "format": "bestaudio/best",
    "extractaudio": True,
    "audioformat": "mp3",
    "outtmpl": "%(title)s.%(ext)s",
    "quiet": True,
    "no_warnings": True,
}

@bot.message_handler(commands=["SPOTIFY"])
def download_song(message):
    query = message.text[len("/SPOTIFY "):].strip()
    if not query:
        bot.reply_to(message, "❌ Please provide a song name or Spotify URL.🫵")
        return

    bot.send_chat_action(message.chat.id, "typing")
    thread = threading.Thread(target=process_song_request, args=(message, query))
    thread.start()

def process_song_request(message, query):
    """Process song request from name or Spotify URL."""
    progress_message = bot.reply_to(message, "⏳ Searching for your song...💯")

    # Check if the query is a Spotify URL
    if "open.spotify.com" in query:
        try:
            # Extract Spotify track details
            track_id = query.split("/")[-1].split("?")[0]
            track = sp.track(track_id)
            track_name = track["name"]
            artist_name = track["artists"][0]["name"]
            full_query = f"{track_name} {artist_name}"
        except Exception as e:
            logger.error(f"Spotify error: {e}")
            bot.edit_message_text(
                "❌ Failed to fetch song details from Spotify. Please try again.🤷",
                chat_id=progress_message.chat.id,
                message_id=progress_message.message_id,
            )
            return
    else:
        full_query = query

    # Search and download song
    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            logger.info(f"Searching for: {full_query}")
            result = ydl.extract_info(f"ytsearch:{full_query}", download=False)["entries"][0]
            song_url = result["webpage_url"]

            # Add buttons for actions
            markup = types.InlineKeyboardMarkup()
            download_button = types.InlineKeyboardButton("⬇️ Download Song", callback_data=f"download|{song_url}")
            cancel_button = types.InlineKeyboardButton("❌ Cancel", callback_data="cancel")
            markup.add(download_button, cancel_button)

            bot.edit_message_text(
                f"🎵 Song found: {result['title']}\n\n"
                f"Artist: {result['uploader']}\n"
                f"Duration: {result['duration']} seconds",
                chat_id=progress_message.chat.id,
                message_id=progress_message.message_id,
                reply_markup=markup,
            )
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.edit_message_text(
            "❌ Failed to find or download the song. Please try again.🫵",
            chat_id=progress_message.chat.id,
            message_id=progress_message.message_id,
        )

# Callback handler for buttons
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data.startswith("download|"):
        song_url = call.data.split("|")[1]
        bot.answer_callback_query(call.id, "⏳ Downloading your song...👀")
        thread = threading.Thread(target=download_and_send_song, args=(call, song_url))
        thread.start()
    elif call.data == "cancel":
        bot.answer_callback_query(call.id, "❌ Cancelled.🤐")
        bot.edit_message_text("❌ Song download cancelled.🤐", chat_id=call.message.chat.id, message_id=call.message.message_id)

def download_and_send_song(call, song_url):
    """Download the song and send it to the user."""
    try:
        with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(song_url, download=True)
            file_name = ydl.prepare_filename(info)

            with open(file_name, "rb") as audio:
                bot.send_audio(
                    chat_id=call.message.chat.id,
                    audio=audio,
                    title=info.get("title", "Unknown Title"),
                    performer=info.get("uploader", "Unknown Artist"),
                )

            bot.edit_message_text("🎉 Your song has been downloaded and sent!😸", chat_id=call.message.chat.id, message_id=call.message.message_id)
            os.remove(file_name)
    except Exception as e:
        logger.error(f"Error: {e}")
        bot.edit_message_text(
            "❌ Failed to download the song. Please try again later.😿",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
        )
@bot.message_handler(commands=["YOUTUBE"])
def process_link(message):
    url = message.text[len("/YOUTUBE "):].strip()
    if not url:
        bot.reply_to(message, "❌ Please provide a valid link.❌")
        return

    if is_valid_instagram_url(url):
        process_instagram_link(message, url)
    elif "youtube.com" in url or "youtu.be" in url:
        process_youtube_link(message, url)
    else:
        bot.reply_to(message, "❌ Unsupported link format.❌")
        

def process_instagram_link(message, url):
    shortcode = extract_instagram_shortcode(url)
    if not shortcode:
        bot.reply_to(message, "❌ Invalid Instagram URL.❌")
        return

    reel_url = fetch_instagram_reel(shortcode)
    if not reel_url:
        bot.reply_to(message, "❌ Could not fetch the reel. Ensure it is public.❌")
        return

    try:
        file_name = f"downloads/reel_{message.chat.id}.mp4"
        response = requests.get(reel_url, stream=True)
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(1024 * 1024):  # 1 MB chunks
                f.write(chunk)

        # Open the file and send it to the user
        with open(file_name, "rb") as video:
            bot.send_video(message.chat.id, video, caption="Here is your downloaded Instagram Reel!")
        os.remove(file_name)

    except Exception as e:
        bot.reply_to(message, f"❌ Failed to download the reel: {str(e)}")

def process_youtube_link(message, url):
    ydl_opts = {
        "format": "best",
        "outtmpl": "downloads/%(title)s.%(ext)s",
        "http_chunk_size": 1048576,
        "progress_hooks": [lambda d: progress_hook(d, message.chat.id)],
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        # Open the downloaded video and send it to the user
        with open(file_name, "rb") as video:
            bot.send_video(message.chat.id, video, caption="Here is your downloaded YouTube video!💘")
        os.remove(file_name)
    except Exception as e:
        bot.reply_to(message, f"❌ Failed to download the video: {str(e)}😰")

def progress_hook(d, chat_id=None):
    if d["status"] == "downloading":
        logger.info(f"Downloading: {d['filename']} - {d['downloaded_bytes'] / d['total_bytes'] * 100:.2f}%")
    elif d["status"] == "finished":
        logger.info(f"Download finished: {d['filename']}")
        if chat_id:
            bot.send_message(chat_id, f"✅ Download completed: {d['filename']}")



# Instaloader setup
loader = Instaloader()
SESSION_FILE = f"{os.getcwd()}/session-{INSTAGRAM_USERNAME}"
session_lock = threading.Lock()

# Load or create Instagram session
def load_or_create_session():
    with session_lock:
        if os.path.exists(SESSION_FILE):
            loader.load_session_from_file(INSTAGRAM_USERNAME, filename=SESSION_FILE)
        else:
            loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
            loader.save_session_to_file(SESSION_FILE)

load_or_create_session()

# Helper functions
def extract_shortcode(url):
    """Extract shortcode from Instagram URL."""
    match = re.search(r"instagram\.com/(?:p|reel|tv)/([^/?#&]+)", url)
    return match.group(1) if match else None
def extract_instagram_shortcode(url):
    """
    Extract the shortcode from an Instagram URL.
    
    Args:
        url (str): The Instagram URL.
        
    Returns:
        str: The extracted shortcode, or None if the URL is invalid.
    """
    # Regex to match Instagram shortcode patterns
    match = re.search(r"instagram\.com/(p|reel|tv)/([a-zA-Z0-9_-]+)/?", url)
    if match:
        return match.group(2)  # Return the shortcode part of the URL
    return None

def is_valid_instagram_url(url):
    """Validate Instagram URL."""
    return bool(re.match(r"https?://(www\.)?instagram\.com/(p|reel|tv)/", url))

def fetch_instagram_reel(shortcode):
    """Fetch Instagram reel media URL."""
    try:
        post = Post.from_shortcode(loader.context, shortcode)
        if post.is_video:
            return post.video_url
        else:
            return None
    except Exception as e:
        logger.error(f"Error fetching Instagram reel: {e}")
        return None
@bot.message_handler(func=lambda message: is_valid_instagram_url(message.text))
def download_reel(message):
    thread = threading.Thread(target=process_download, args=(message,))
    thread.start()

def process_download(message):
    bot.send_chat_action(message.chat.id, "typing")
    progress_message = bot.reply_to(message, "⏳ Fetching your reel...🧐")
    url = message.text.strip()
    shortcode = extract_shortcode(url)

    if not shortcode:
        bot.edit_message_text("❌ Invalid Instagram URL. Please send a valid reel link.🫵", chat_id=progress_message.chat.id, message_id=progress_message.message_id)
        return

    reel_url = fetch_instagram_reel(shortcode)
    if not reel_url:
        bot.edit_message_text("❌ Failed to fetch the reel. Ensure the reel is public and try again.🫵 ", chat_id=progress_message.chat.id, message_id=progress_message.message_id)
        return

    file_name = f"reel_{message.chat.id}.mp4"
    try:
        response = requests.get(reel_url, stream=True)
        response.raise_for_status()  # Raises HTTPError for bad responses
        with open(file_name, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                f.write(chunk)

        with open(file_name, "rb") as video:
            bot.send_video(chat_id=message.chat.id, video=video, caption="👾 Here is your reel! Powered by @clutch008\nFEEL FREE TO EXPLORE MORE")
        bot.delete_message(chat_id=progress_message.chat.id, message_id=progress_message.message_id)
    except Exception as e:
        logger.error(f"Error sending reel: {e}")
        bot.edit_message_text("❌ Failed to send the reel. Please try again later\nPRIVATE VIDEOS NOT SUPPORTED !.", chat_id=progress_message.chat.id, message_id=progress_message.message_id)
    finally:
        if os.path.exists(file_name):
            os.remove(file_name)

# Main function
if __name__ == "__main__":
    logger.info("Bot is running...🤖 DEVELOPED BY ABHINAI")
    bot.infinity_polling()