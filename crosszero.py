import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
import asyncio

# Логирование поможет увидеть ошибки в консоли, если они повяятся
logging.basicConfig(level=logging.INFO)

# Твой токен (не меняем)
BOT_TOKEN = '8550093450:AAG1pJ65r81PQpzyy81Vzvn2wk_IlmlN2F4' 


MINI_APP_URL = 'https://nikitaaks.github.io/CrossZeroGame/'

async def start_command(message: types.Message):
    # Используем переменную MINI_APP_URL, чтобы менять адрес только в одном месте
    webapp_info = types.WebAppInfo(url=MINI_APP_URL)
    
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="🚀 Открыть игру крестики-нолики", web_app=webapp_info)]
    ])

    user_name = message.from_user.first_name if message.from_user else "Игрок"

    await message.answer(
        f"Привет, {user_name}! Нажми на кнопку ниже, чтобы запустить приложение.",
        reply_markup=keyboard
    )

async def web_app_data_handler(message: types.Message):
    game_result = message.web_app_data.data # 'win X', 'win O', 'draw'
    user_name = message.from_user.first_name if message.from_user.first_name else "Игрок"

    if game_result.startswith('win'):
        winner = game_result.split(' ')[1]
        await message.answer(f"Поздравляем, {user_name}! Игрок {winner} победил в Крестиках-ноликах!")
    elif game_result == 'draw':
        await message.answer(f"Игра Крестики-нолики завершилась вничью, {user_name}!")
    else:
        await message.answer(f"Получен результат игры: {game_result}")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    
    # Регистрация хэндлера
    dp.message.register(start_command, CommandStart())
    dp.message.register(web_app_data_handler, F.content_type == 'web_app_data')

    logging.info("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logging.info("Бот остановлен")