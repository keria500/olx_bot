from aiogram import Router, F
from aiogram.types import Message

from bot.keyboards import start_keyboard

router = Router()

@router.message(F.text == "/start")
async def Start(message: Message):
    await message.answer("Старт", reply_markup=start_keyboard())
