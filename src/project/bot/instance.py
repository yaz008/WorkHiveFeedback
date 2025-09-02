from telebot import TeleBot

from project.env import Env


bot: TeleBot = TeleBot(
    token=Env.TELEGRAM_BOT_TOKEN,
    parse_mode='HTML',
    skip_pending=True,
    threaded=False,
    num_threads=1,
)
