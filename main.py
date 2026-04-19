import asyncio
import logging
import sys
from os import getenv
from pathlib import Path

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from dotenv import load_dotenv

from keyboards.reply_keyboards import get_searchion_keyboard
from keyboards.inline_keyboards import get_inline_hs
from handlers import register_handlers


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()
register_handlers(dp)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Привіт, {html.bold(message.from_user.full_name)}!\n"
                         "HireNow – бот для пошуку роботи в IT-сфері.", reply_markup=get_searchion_keyboard())
    await message.answer(f"Він допомагає працівникам знайти вакансії за їхніми навичками, а роботодавцям – швидко знаходити кваліфікованих спеціалістів. "
                         "Вибери хто ти, Роботодавець чи працівник?",
                         reply_markup=get_inline_hs())


async def main() -> None:
    if not TOKEN:
        raise RuntimeError("BOT_TOKEN is not set")

    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
