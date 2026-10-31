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
MY_USER_ID = 1029773942  # Твой ID для автоматических уведомлений в личку
RENDER_URL = "https://date-bot-3aj8.onrender.com"
WEBHOOK_PATH = f"/bot/{TOKEN}"
WEBHOOK_URL = f"{RENDER_URL}{WEBHOOK_PATH}"

ALLOWED_USER_IDS = [1067015608, MY_USER_ID]

MOMENTS = [
    "✨ Момент 1 из 10\n\nЛюбимая, эта неделя особенная, совсем как ты. Спасибо за то, что ты у меня есть! 🥰",
    "✨ Момент 2 из 10\n\nКаждый день с тобой — это отдельное маленькое приключение. ❤️",
    "✨ Момент 3 из 10\n\nДаже в самый пасмурный день рядом с тобой тепло и уютно. ✨",
    "✨ Момент 4 из 10\n\nКрасотка моя! Самые лучшие моменты только с тобой. 💫",
    "✨ Момент 5 из 10\n\nРядом с тобой мир становится ярче. 🌸",
    "✨ Момент 6 из 10\n\nСамые нежные и сладкие воспоминания. 💕",
    "✨ Момент 7 из 10\n\nНаша романтика и прогулки по самым красивым местам. 🌿",
    "✨ Момент 8 из 10\n\nУлыбайся чаще, твоя улыбка бесценна! 🥰",
    "✨ Момент 9 из 10\n\nВместе мы команда в любых ситуациях — даже за бильярдным столом! 🎱❤️",
    "✨ Момент 10 из 10\n\nЧуть позже добавлю что-то еще... А пока просто знай, как сильно я тебя люблю! 🥰❤️"
]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USER_IDS

# Клавиатуры
def get_intro_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="✨ Идем дальше ❤️", callback_data="intro_yes")
    b.button(text="❌ Не хочу / Неинтересно", callback_data="intro_no")
    b.adjust(1)
    return b.as_markup()

def get_main_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="💌 Выбрать свидание", callback_data="menu_dates")
    b.button(text="📸 Наши моменты и сюрприз", callback_data="moment_0")
    b.button(text="🎧 Музыкальный вайб ✨", callback_data="music_menu")  # <--- Добавили музыкальную кнопку
    b.button(text="⬅️ Назад к началу", callback_data="back_to_intro")
    b.adjust(1)
    return b.as_markup()

def get_date_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🎬 Кино", callback_data="sub_cinema")
    b.button(text="🍷 Ужин", callback_data="sub_dinner")
    b.button(text="🌙 Прогулка", callback_data="sub_walk")
    b.button(text="🎁 Секретный вариант", callback_data="final_secret")
    b.button(text="⬅️ Назад в меню", callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()

# Музыкальное меню с категориями
def get_music_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🔥 Драйв и Энергия", callback_data="music_drive")
    b.button(text="✨ Атмосфера и Вайб", callback_data="music_vibe")
    b.button(text="⬅️ Назад в меню", callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()

def get_music_back_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ К музыкальному меню", callback_data="music_menu")
    b.adjust(1)
    return b.as_markup()

# Подменю: Кино
def get_cinema_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🍿 Комедия", callback_data="final_cinema_comedy")
    b.button(text="😱 Ужасы", callback_data="final_cinema_horror")
    b.button(text="💖 Мелодрама", callback_data="final_cinema_romance")
    b.button(text="🔥 Экшен / Боевик", callback_data="final_cinema_action")
    b.button(text="⬅️ Назад к выбору", callback_data="menu_dates")
    b.adjust(1)
    return b.as_markup()

# Подменю: Ужин
def get_dinner_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🏠 Дома (уютный вечер)", callback_data="final_dinner_home")
    b.button(text="🍽️ В ресторане", callback_data="final_dinner_restaurant")
    b.button(text="🧺 Пикник", callback_data="final_dinner_picnic")
    b.button(text="🌆 На крыше", callback_data="final_dinner_roof")
    b.button(text="⬅️ Назад к выбору", callback_data="menu_dates")
    b.adjust(1)
    return b.as_markup()

# Подменю: Прогулка
def get_walk_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🏛️ По ночному Кракову", callback_data="final_walk_krakow")
    b.button(text="🌲 В парке / лесу", callback_data="final_walk_nature")
    b.button(text="⬅️ Назад к выбору", callback_data="menu_dates")
    b.adjust(1)
    return b.as_markup()

def get_contact_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="💬 Написать ему лично ❤️", url=f"https://t.me/{MY_TELEGRAM}")
    b.button(text="⬅️ Выбрать что-то еще", callback_data="menu_dates")
    b.adjust(1)
    return b.as_markup()

# Обработчики
@dp.message(Command("start"))
async def cmd_start(msg: types.Message):
    if not is_allowed(msg.from_user.id):
        await msg.answer("🔒 Упс! Этот бот является личным и секретным проектом. Доступ ограничен. ❤️")
        return
    await msg.answer(
        "Привет, моя любимая! 🥰 Смотри, что я тут для тебя создал. "
        "Надеюсь, тебе понравится этот небольшой сюрприз!\n\nНу что, готовы двигаться дальше?",
        reply_markup=get_intro_keyboard()
    )

@dp.callback_query(F.data == "intro_yes")
async def intro_yes(c: types.CallbackQuery):
    await c.message.edit_text(
        "Отличный выбор
