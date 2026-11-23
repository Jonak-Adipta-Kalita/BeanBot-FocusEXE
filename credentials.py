import os
from dotenv import load_dotenv

load_dotenv()
config = os.getenv

TOKEN = config("BOT_TOKEN")
SERVER_CHANNEL_ID = config("SERVER_CHANNEL_ID")
