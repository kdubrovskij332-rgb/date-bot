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
    builder.button(text="Хм, я сомневаюсь...", callback_data="exit_no")
    builder.adjust(1)
    return builder.as_markup()

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💌 Выбрать свидание", callback_data="menu_dates")
    builder.button(text="📸 Наши моменты и сюрприз", callback_data="moment_0")
    builder.adjust(1)
    return builder.as_markup()

def get_date_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="🎬 Кино", callback_data="date_cinema")
    builder.button(text="🌙 Прогулка", callback_data="date_walk")
    builder.button(text="🍷 Романтический ужин", callback_data="date_dinner")
    builder.button(text="🎁 Секретный вариант", callback_data="date_secret")
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

def get_contact_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💬 Написать о согласии ❤️", url=f"https://t.me/{MY_TELEGRAM}")
    builder.button(text="⬅️ В меню", callback_data="back_to_main")
    builder.adjust(1)
    return builder.as_markup()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    if not is_allowed(user_id):
        await message.answer("🔒 Упс! Этот бот является личным и секретным проектом. Доступ ограничен. ❤️")
        return

    await message.answer(
        "Привет, моя любимая! 🥰 Смотри, что я тут для тебя создал. "
        "Надеюсь, тебе понравится этот небольшой сюрприз!\n\nНу что, готовы двигаться дальше?",
        reply_markup=get_intro_keyboard()
    )

@dp.callback_query(F.data == "intro_yes")
async def process_intro_yes(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Отличный выбор! Я знал, что тебе понравится. 💫\n\n"
        "Добро пожаловать в наш личный уголок. Выбирай, что тебе хочется посмотреть:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "intro_no")
async def process_intro_no(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Ого... Ты уверена, что хочешь всё закончить прямо сейчас?",
        reply_markup=get_exit_confirm_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "exit_yes")
async def process_exit_yes(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "А я тебе не дам этого сделать! 😉 Слишком долго я это для тебя готовил. Давай-ка по новой! ❤️",
        reply_markup=get_intro_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "exit_no")
async def process_exit_no(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Отлично, я так и знал! 🥰 Ты же у меня самая любопытная. Пойдем скорее смотреть, что там внутри! ✨",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data == "menu_dates")
async def process_menu_dates(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Куда бы ты хотела отправиться на этот раз?",
        reply_markup=get_date_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("moment_"))
async def process_moment_navigation(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[1])
    text = MOMENTS[index]
    
    builder = InlineKeyboardBuilder()
    if index > 0:
        builder.button(text="⬅️ Назад", callback_data=f"moment_{index - 1}")
    if index < len(MOMENTS) - 1:
        builder.button(text="Вперед ➡️", callback_data=f"moment_{index + 1}")
        
    builder.button(text="🏠 Главное меню", callback_data="back_to_main")
    builder.adjust(2, 1)
    
    await callback.
