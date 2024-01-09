import warnings

import telegram

warnings.filterwarnings("ignore", category=DeprecationWarning)

bot = telegram.Bot(bot_token)