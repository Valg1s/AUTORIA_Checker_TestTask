import warnings

import telegram

warnings.filterwarnings("ignore", category=DeprecationWarning)

bot_token = "6839765662:AAFx6GS-iK9o6prGM3g8YQV3T4kj1rdm6WI"
chat_id = "-1001630405073"

bot = telegram.Bot(bot_token)

from . import searchers