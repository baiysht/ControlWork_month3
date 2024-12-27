# info_command

from aiogram import types, Dispatcher
from config import bot

async def info_handler(message: types.Message):
    await bot.send_message(chat_id=message.from_user.id,
                           text='Я бот онлайн магазина обуви!\n'
                                'Ты можешь:\n'
                                '* Просмотреть обувь коммандой: /products\n'
                                '* Сделать заказ коммандой: /buy')


def register_info_handlers(dp: Dispatcher):
    dp.register_message_handler(info_handler, commands=["info"])