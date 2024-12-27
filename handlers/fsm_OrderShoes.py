# fsm_OrderShoes.py

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from buttons import cancel_markup, start_markup
from config import bot, Staff


class FSMOrder(StatesGroup):
    Product_id = State()
    Product_size = State()
    Quantity = State()
    Contacts = State()
    Submit = State()


async def start_fsm_OrderShoes(message: types.Message):
    await message.answer('Введите артикул товара который хотите заказать:', reply_markup=cancel_markup)
    await FSMOrder.Product_id.set()

async def load_product_id(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_id'] = message.text


    await FSMOrder.next()
    await message.answer('Введите размер товара:', reply_markup=cancel_markup)

async def load_product_size(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['product_size'] = message.text


    await FSMOrder.next()
    await message.answer('Введите кол-во товара:', reply_markup=cancel_markup)

async def load_quantity(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['quantity'] = message.text


    await FSMOrder.next()
    await message.answer('Введите свои контакты:', reply_markup=cancel_markup)

async def load_contacts(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['contacts'] = message.text


    await FSMOrder.next()
    await message.answer(f'Верные ли данные?\n'
                         f'Артикул - {data["product_id"]}\n'
                         f'Размер - {data["product_size"]}\n'
                         f'Количество - {data["quantity"]}\n'
                         f'Контакты - {data["contacts"]}')

async def load_submit(message: types.Message, state: FSMContext):
    if message.text == 'Да':
        async with state.proxy() as data:
            for user_id in Staff:
                try:
                    await bot.send_message(chat_id=user_id, text=f'Новый заказ:\n'
                                                    f'Артикул товара: {data["product_id"]}\n'
                                                    f'Размер товара: {data["product_size"]}\n'
                                                    f'Количество товара: {data["quantity"]}\n'
                                                    f'Номер телефона клиента: {data["contacts"]}')
                except Exception as error:
                    print(f"Не удалось отправить сообщение пользователю {user_id}: {error}")

        await message.answer('Ваш заказ отправлен! Мы свяжемся с вами в ближайшее время.')
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
        await message.answer( Text='Отмененно!', reply_markup=start_markup)


def register_fsm_OrderShoes_handlers(dp: Dispatcher):
    dp.register_message_handler(cancel_fsm, Text(equals='Отмена',
                                                 ignore_case=True), state='*')

    dp.register_message_handler(start_fsm_OrderShoes, commands=['buy'])
    dp.register_message_handler(load_product_id, state=FSMOrder.Product_id)
    dp.register_message_handler(load_product_size, state=FSMOrder.Product_size)
    dp.register_message_handler(load_quantity, state=FSMOrder.Quantity)
    dp.register_message_handler(load_contacts, state=FSMOrder.Contacts)
    dp.register_message_handler(load_submit, state=FSMOrder.Submit)