# fsm_NewShoes.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel_markup, start_markup
from db import main_db


class FSMShop(StatesGroup):
    Name_product = State()
    Category = State()
    Product_size = State()
    Price = State()
    Product_id = State()
    Photo = State()
    Submit = State()


async def start_fsm_NewShoes(message: types.Message):
    await message.answer('Введите название модели:', reply_markup=cancel_markup)
    await FSMShop.Name_product.set()

async def load_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name_product'] = message.text


    await FSMShop.next()
    await message.answer('Введите категорию товара:', reply_markup=cancel_markup)

async def load_category(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['category'] = message.text


    await FSMShop.next()
    await message.answer('Введите размеры товара:', reply_markup=cancel_markup)

async def load_product_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_size'] = message.text

    await FSMShop.next()
    await message.answer('Введите цену товара:', reply_markup=cancel_markup)

async def load_price(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['price'] = message.text


    await  FSMShop.next()
    await message.answer('Укажите id товара:', reply_markup=cancel_markup)

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text


    await FSMShop.next()
    await message.answer('Отправьте фото товара:', reply_markup=cancel_markup)

async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['photo'] = message.photo[-1].file_id


    await FSMShop.next()
    await message.answer(f'Верные ли данные?')
    await message.answer_photo(photo=data['photo'],
                               caption=f'Название модели - {data["name_product"]}\n'
                                       f'Категория - {data["category"]}\n'
                                       f'Размеры - {data["product_size"]}\n'
                                       f'Цена - {data["price"]}\n'
                                       f'Артикул товара - {data["product_id"]}')

async def load_submit(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            await main_db.sql_insert_products(
                name_product=data['name_product'],
                category=data['category'],
                product_size=data['product_size'],
                price=data['price'],
                product_id=data['product_id'],
                photo=data['photo']
            )
            await message.answer('Ваши данные в базе!')
            await state.finish()

    elif message.text == 'Нет':
        await message.answer('Хорошо, отменено!')
        await state.finish()

    else:
        await message.answer('Вводите только Да или Нет!')


async def cancel_fsm(message: types.Message, state: FSMContext):
    current_state = await state.get_state()

    if current_state is not None:
        await state.finish()
        await message.answer('Отменено!', reply_markup=start_markup)


def register_fsm_NewShoes_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True), state='*')

    dp.register_message_handler(start_fsm_NewShoes, commands=['new_product'])
    dp.register_message_handler(load_name_product, state=FSMShop.Name_product)
    dp.register_message_handler(load_category, state=FSMShop.Category)
    dp.register_message_handler(load_product_size, state=FSMShop.Product_size)
    dp.register_message_handler(load_price, state=FSMShop.Price)
    dp.register_message_handler(load_product_id, state=FSMShop.Product_id)
    dp.register_message_handler(load_photo, state=FSMShop.Photo, content_types=['photo'])
    dp.register_message_handler(load_submit, state=FSMShop.Submit)