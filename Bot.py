import os
import logging
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "9087803060:AAHc7yBMYPT7FFWzEP7zXjuV66XsPBiz3xI"
MY_TELEGRAM = "RichiHons"

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

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

# Простейший веб-сервер для Render, который удовлетворяет требованиям хостинга
async def handle(request):
    return web.Response(text="Bot is alive and running!")

app = web.Application()
app.router.add_get("/", handle)

async def on_startup(app):
    # Удаляем вебхуки на всякий случай, чтобы не было конфликтов getUpdates
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем поллинг в фоновом режиме
    import asyncio
    asyncio.create_task(dp.start_polling(bot))

app.on_startup.append(on_startup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
