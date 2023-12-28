from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
)

open_ticket_kb = InlineKeyboardMarkup(inline_keyboard=[[
    InlineKeyboardButton(text='Задать вопрос', callback_data='open_ticket')
]])
