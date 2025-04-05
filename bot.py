import asyncio
import random
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.filters import Command
from aiogram.client.default import DefaultBotProperties
from api import TOKEN, API_FILMS

# Создаем объект - бот и диспетчер
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
dp = Dispatcher()

# Основная клавиатура
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Привет!"), KeyboardButton(text="Помощь")]
    ],
    resize_keyboard=True
)

# Инлайн клавиатура
inline_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Начать", callback_data="start")],
        [InlineKeyboardButton(text="Помощь", callback_data="help")],
    ]
)

# Функция для получения данных о фильме по названию
async def get_movie_by_title(title: str):
    url = f"{API_FILMS}/movie/{title}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={'apikey': TOKEN}) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None

# Функция для получения случайного фильма или сериала
async def get_random_movie_or_series():
    url = f"{API_FILMS}/random"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params={'apikey': TOKEN}) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                return None


# Приветствие
@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Я тестовый бот <b>test</b>", reply_markup=main_keyboard)

# Команда для получения информации о фильме по названию
@dp.message(Command("film_info"))
async def film_info_command(message: types.Message):
    title = message.text[10:].strip()
    if not title:
        await message.answer("Пожалуйста, укажите название фильма.")
        return

    movie = await get_movie_by_title(title)
    if movie:
        await message.answer(f"Фильм: {movie['title']}\nОписание: {movie['description']}")
    else:
        await message.answer(f"Не удалось найти фильм с названием {title}.")

# Команда для случайного фильма/сериала
@dp.message(Command("random_movie_or_series"))
async def random_movie_or_series_command(message: types.Message):
    movie_or_series = await get_random_movie_or_series()
    if movie_or_series:
        await message.answer(f"Случайный фильм/сериал: {movie_or_series['title']}\nОписание: {movie_or_series['description']}")
    else:
        await message.answer("Не удалось получить случайный фильм или сериал.")


# Помощь
@dp.message(Command("help"))
async def help_command(message: types.Message):
    command_text = (
        "Доступные команды:\n"
        "/start - начать работу с ботом\n"
        "/help - Показывает список команд\n"
        "/random - Генерирует рандомное число\n"
        "/film_info <название> - Получить информацию о фильме по названию\n"
        "/random_movie_or_series - Получить случайный фильм или сериал\n"
        "/random_by_genre <жанр> - Получить случайный фильм или сериал по жанру\n"
    )
    await message.answer(command_text)

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())