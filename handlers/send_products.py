# send_products

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from db import main_db


async def start_send_products(message: types.Message):
    keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
    button_all_products = types.InlineKeyboardButton('Вывести все товары',
                                                     callback_data='send_all_products')

    keyboard.add(button_all_products)

    await message.answer('Выберите как просмотреть товары:', reply_markup=keyboard)

async def send_all_products(call: types.CallbackQuery):
    products = main_db.fetch_all_products()

    if products: # True
        for product in products:
            caption = (f'Название - {product["name_product"]}\n'
            f'Категория - {product["category"]}\n'
            f'Размер - {product["product_size"]}\n'
            f'Цена - {product["price"]}\n'
            f'Артикул - {product["product_id"]}')


            await call.message.answer_photo(photo=product['photo'], caption=caption)
    else: # False
        await call.message.answer('База пустая! Товаров нет.')


def register_handlers(dp: Dispatcher):
    dp.register_message_handler(start_send_products, commands=['products'])
    dp.register_callback_query_handler(send_all_products, Text(equals='send_all_products'))