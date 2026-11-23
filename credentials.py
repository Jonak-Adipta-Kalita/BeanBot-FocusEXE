import os
from dotenv import load_dotenv

load_dotenv()
config = os.getenv

TOKEN = config("BOT_TOKEN")
SERVER_ID = int(config("SERVER_ID"))
SERVER_CHANNEL_ID = int(config("SERVER_CHANNEL_ID"))
