import asyncio
import os
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

# 1. Токен твоего бота
TOKEN = "9087803060:AAHc7yBMYPT7FFWzEP7zXjuV66XsPBiz3xI"

# 2. Твой ник в Тг БЕЗ собаки @
MY_TELEGRAM = "RichiHons"  

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- Веб-сервер для Render ---
async def handle(request):
    return web.Response(text="Bot is alive!")

app = web.Application()
app.router.add_get("/", handle)

async def start_web_server():
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")
# -----------------------------

def get_date_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎬 Кино", callback_data="date_cinema")
    builder.button(text="🌙 Прогулка", callback_data="date_walk")
    builder.button(text="🍷 Романтический ужин", callback_data="date_dinner")
    builder.button(text="🎁 Секретный вариант", callback_data="date_secret")
    builder.adjust(1)
    return builder.as_markup()

def get_contact_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Написать о согласии ❤️", url=f"https://t.me/{MY_TELEGRAM}")
    return builder.as_markup()

@dp.message(Command("start", "date"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет, моя любимая! 🥰 У меня есть к тебе важное предложение. "
        "Куда бы ты хотела отправиться на этот раз?",
        reply_markup=get_date_keyboard()
    )

@dp.callback_query(F.data == "date_cinema")
async def process_cinema(callback: types.CallbackQuery):
    await callback.message.answer(
        "🎬 Отличный выбор! Пойдем на классный фильм с попкорном и самыми удобными местами. Жду не дождусь! ❤️\n\n"
        "Ну что, идем?",
        reply_markup=get_contact_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "date_walk")
async def process_walk(callback: types.CallbackQuery):
    await callback.message.answer(
        "🌙 Ночная прогулка под звездами, теплая атмосфера и только мы вдвоем. Идеально! ✨\n\n"
        "Согласна?",
        reply_markup=get_contact_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "date_dinner")
async def process_dinner(callback: types.CallbackQuery):
    await callback.message.answer(
        "🍷 Романтический ужин, вкусная еда, красивые свечи и потрясающая компания. Жду тебя! 🍝\n\n"
        "Идем?",
        reply_markup=get_contact_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "date_secret")
async def process_secret(callback: types.CallbackQuery):
    await callback.message.answer(
        "🎁 Ого, выбор интригует! Это будет сюрприз, о котором ты точно не пожалеешь. Подсказка: бери хорошее настроение! 😉\n\n"
        "Рискнем?",
        reply_markup=get_contact_keyboard()
    )
    await callback.answer()

async def main():
    # Запускаем и веб-сервер, и бота одновременно
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
