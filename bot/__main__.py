import asyncio
import logging
from aiogram import Dispatcher, Bot
from bot.config import TOKEN
from bot.handlers import admin
from bot.misc import commands_for_bot


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)


    dp = Dispatcher()
    bot = Bot(token=TOKEN)

    dp.include_router(router=admin)

    await bot.set_my_commands(commands=commands_for_bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main=main())