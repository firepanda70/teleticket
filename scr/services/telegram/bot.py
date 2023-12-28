from aiogram import Bot
from aiogram.enums import ParseMode

from scr.core.config import settings
from .messages_const import PROGRESS_TCKET_MSG, TICKET_CLOSED_MSG
from .kb import open_ticket_kb


bot = Bot(token=settings.bot_token, parse_mode=ParseMode.HTML)


async def send_progress_notification(tg_user_id: int, user_id: int):
    await bot.send_message(tg_user_id, PROGRESS_TCKET_MSG.format(user_id))


async def send_closed_notification(tg_user_id: int):
    await bot.send_message(
        tg_user_id, TICKET_CLOSED_MSG,
        reply_markup=open_ticket_kb
    )


async def send_reply(tg_user_id: int, text: str):
    await bot.send_message(tg_user_id, text)
