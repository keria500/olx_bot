from bot.handlers import router

from aiogram import Dispatcher, Bot

from config import config

bot = Bot(token=config.bot_token)
dp = Dispatcher()
dp.include_router(router)
