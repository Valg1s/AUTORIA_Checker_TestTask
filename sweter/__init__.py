import warnings
import os

import telegram
import dotenv

dotenv.load_dotenv()

warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

bot_token = os.getenv("bot_token")
chat_id = os.getenv("chat_id")

bot = telegram.Bot(bot_token)

from . import searchers