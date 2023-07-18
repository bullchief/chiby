from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

start_keyboard = InlineKeyboardBuilder()
start_keyboard.row(
    types.InlineKeyboardButton(text="Перейти на канал", url="https://t.me/xdev_v"),
    types.InlineKeyboardButton(text="Начать чат", callback_data="check_subscribe")
)