import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiohttp import web

TOKEN = "9087803060:AAHc7yBMYPT7FFWzEP7zXjuV66XsPBiz3xI"
MY_TELEGRAM = "RichiHons"
MY_USER_ID = 1029773942
RENDER_URL = "https://date-bot-3aj8.onrender.com"
WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = f"{RENDER_URL}{WEBHOOK_PATH}"

ALLOWED_USER_IDS = [1067015608, MY_USER_ID]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="💌 Выбрать свидание", callback_data="menu_dates")
    b.button(text="🎧 Музыкальный вайб ✨", callback_data="music_menu")
    b.adjust(1)
    return b.as_markup()

def get_music_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🔥 Драйв и Энергия", callback_data="music_drive")
    b.button(text="✨ Атмосфера и Вайб", callback_data="music_vibe")
    b.button(text="⬅️ Назад в меню", callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()

@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    if msg.from_user.id not in ALLOWED_USER_IDS:
        await msg.answer("🔒 Доступ ограничен ❤️")
        return
    await msg.answer(
        "Привет, моя любимая! Выбирай, что тебе хочется:",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data == "music_menu")
async def music_menu(c: types.CallbackQuery):
    await c.message.edit_text("🎧 Выбери настроение:", reply_markup=get_music_keyboard())
    await c.answer()

@dp.callback_query(F.data == "music_drive")
async def music_drive(c: types.CallbackQuery):
    text = "🔥 **Драйв и Энергия:**\n\n1. Instasamka — Эверест\n2. Dead Blonde — Казино"
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ К меню музыки", callback_data="music_menu")
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "music_vibe")
async def music_vibe(c: types.CallbackQuery):
    text = "✨ **Атмосфера и Вайб:**\n\n1. Игнатов — Мое тело — убийца"
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ К меню музыки", callback_data="music_menu")
    await c.message.edit_text(text, reply_markup=b.as_markup(), parse_mode="Markdown")
    await c.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_main(c: types.CallbackQuery):
    await c.message.edit_text("Главное меню ❤️", reply_markup=get_main_keyboard())
    await c.answer()

async def handle_webhook(request: web.Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_webhook)
app.router.add_get("/", lambda r: web.Response(text="OK"))
app.on_startup.append(on_startup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
