# buttons.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup

start_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
start_markup.add(KeyboardButton('/start'), KeyboardButton('/info'), KeyboardButton('/new_product'),
                 KeyboardButton('/products'), KeyboardButton('/buy'))

cancel_markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
cancel_markup.add(KeyboardButton("Отмена"))