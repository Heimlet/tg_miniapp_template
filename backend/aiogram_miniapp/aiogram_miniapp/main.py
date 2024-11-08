import logging
import sys
from os import getenv
from pathlib import Path

from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from environs import Env

# Инициализация переменных окружения
env = Env()
env.read_env()

BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Получение необходимых переменных из окружения
TOKEN = env('BOT_API_KEY')

WEB_SERVER_HOST = env('WEB_SERVER_HOST', '127.0.0.1')
WEB_SERVER_PORT = env.int('WEB_SERVER_PORT', 8080)
WEBHOOK_PATH = env('WEBHOOK_PATH', '/webhook')
WEBHOOK_SECRET = env('WEBHOOK_SECRET', 'my-secret')
BASE_WEBHOOK_URL = env('BASE_WEBHOOK_URL', 'https://your.public.url')
BOT_MODE = env('BOT_MODE', 'long-polling')

# Инициализация роутера
router = Router()

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    Обработчик команды /start
    """
    await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@router.message()
async def echo_handler(message: Message) -> None:
    """
    Обработчик всех входящих сообщений
    """
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.answer("Nice try!")


async def on_startup(bot: Bot) -> None:
    """
    Устанавливает webhook при старте, если используется webhook
    """
    if BOT_MODE == 'webhook':
        await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)


def main() -> None:
    # Инициализация диспетчера
    dp = Dispatcher()
    dp.include_router(router)

    # Регистрация хука для старта
    dp.startup.register(on_startup)

    # Инициализация бота
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    if BOT_MODE == 'webhook':
        # Режим работы с использованием webhook
        app = web.Application()

        # Настройка SimpleRequestHandler для обработки запросов от Telegram
        webhook_requests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
        )
        webhook_requests_handler.register(app, path=WEBHOOK_PATH)

        # Подключение хуков старта и остановки к aiohttp приложению
        setup_application(app, dp, bot=bot)

        # Запуск веб-сервера
        web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)
    else:
        # Режим работы с использованием long-polling
        dp.run_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    main()
