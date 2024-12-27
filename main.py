# main.py

from aiogram import executor, types
from config import bot, dp, Admins, Staff
import logging
from db import main_db
from handlers import start_command, info_command, fsm_NewShoes, send_products, fsm_OrderShoes
import buttons


async def on_startup(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот включен!',
                               reply_markup=buttons.start_markup)
    await main_db.DataBase_create()

async def on_shutdown(_):
    for admin in Admins:
        await bot.send_message(chat_id=admin, text='Бот выключен!')


start_command.register_start_handlers(dp)
info_command.register_info_handlers(dp)

fsm_NewShoes.register_fsm_NewShoes_handlers(dp)
fsm_OrderShoes.register_fsm_OrderShoes_handlers(dp)

send_products.register_handlers(dp)




if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup,
                           on_shutdown=on_shutdown)