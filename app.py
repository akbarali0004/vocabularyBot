from asyncio import run
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from config import BOT_TOKEN, ADMIN
from handlers import router
from utils import db_start


dp = Dispatcher()


@dp.startup()
async def on_startup(bot:Bot):
    await db_start()
    msg = await bot.send_message(ADMIN, "Bot started")

@dp.shutdown()
async def on_shutdown(bot:Bot):
    await bot.send_message(ADMIN, "Bot stopped")

async def main():
    dp.include_router(router)
    bot = Bot(token=BOT_TOKEN, default = DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.error("Bot stopped!")