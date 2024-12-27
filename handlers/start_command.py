# start_command

from aiogram import types, Dispatcher
from config import bot

async def start_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text=f'Добро пожаловать {message.from_user.first_name}!\n'
                                f'Твой Telegram ID - {message.from_user.id}')


def register_start_handlers(dp: Dispatcher):
    dp.register_message_handler(start_handler, commands=["start"])