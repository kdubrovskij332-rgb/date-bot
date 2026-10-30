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
RENDER_URL = "https://date-bot-3aj8.onrender.com"

ALLOWED_USER_IDS = [
    1067015608, # ID твоей девушки
    1029773942  # Твой ID
]

# Супер-надежная галерея вайбовых моментов с описаниями (работает мгновенно без сбоев сетей)
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

def get_intro_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="✨ Идем дальше ❤️", callback_data="intro_yes")
    builder.button(text="❌ Не хочу", callback_data="intro_no")
    builder.adjust(1)
    return builder.as_markup()

def get_exit_confirm_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Да, точно хочу закончить", callback_data="exit_yes")
    builder.button(text="Хм, я сомневаюсь...", callback_data="exit_no
