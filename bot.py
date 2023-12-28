import asyncio
import logging
import sys

from aiogram import Dispatcher

from scr.services.telegram.bot import bot
from scr.services.telegram.router import router


async def main():
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
