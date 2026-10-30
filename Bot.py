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

ALLOWED_USER_IDS = [1067015608, 1029773942]

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
    b = InlineKeyboardBuilder()
    b.button(text="✨ Идем дальше ❤️", callback_data="intro_yes")
    b.button(text="❌ Не хочу", callback_data="intro_no")
    b.adjust(1)
    return b.as_markup()

def get_exit_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="Да, точно хочу закончить", callback_data="exit_yes")
    b.button(text="Хм, я сомневаюсь...", callback_data="exit_no")
    b.adjust(1)
    return b.as_markup()

def get_main_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="💌 Выбрать свидание", callback_data="menu_dates")
    b.button(text="📸 Наши моменты и сюрприз", callback_data="moment_0")
    b.adjust(1)
    return b.as_markup()

def get_date_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🎬 Кино", callback_data="date_cinema")
    b.button(text="🌙 Прогулка", callback_data="date_walk")
    b.button(text="🍷 Романтический ужин", callback_data="date_dinner")
    b.button(text="🎁 Секретный вариант", callback_data="date_secret")
    b.button(text="⬅️ Назад", callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()

def get_contact_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="💬 Написать о согласии ❤️", url=f"https://t.me/{MY_TELEGRAM}")
    b.button(text="⬅️ В меню", callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()

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
        "Отличный выбор! Я знал, что тебе понравится. 💫\n\n"
        "Добро пожаловать в наш личный уголок. Выбирай, что тебе хочется посмотреть:",
        reply_markup=get_main_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "intro_no")
async def intro_no(c: types.CallbackQuery):
    await c.message.edit_text(
        "Ого... Ты уверена, что хочешь всё закончить прямо сейчас?",
        reply_markup=get_exit_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "exit_yes")
async def exit_yes(c: types.CallbackQuery):
    await c.message.edit_text(
        "А я тебе не дам этого сделать! 😉 Слишком долго я это для тебя готовил. Давай-ка по новой! ❤️",
        reply_markup=get_intro_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "exit_no")
async def exit_no(c: types.CallbackQuery):
    await c.message.edit_text(
        "Отлично, я так и знал! 🥰 Ты же у меня самая любопытная. Пойдем скорее смотреть, что там внутри! ✨",
        reply_markup=get_main_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "menu_dates")
async def menu_dates(c: types.CallbackQuery):
    await c.message.edit_text(
        "Куда бы ты хотела отправиться на этот раз?",
        reply_markup=get_date_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data.startswith("moment_"))
async def moment_nav(c: types.CallbackQuery):
    idx = int(c.data.split("_")[1])
    text = MOMENTS[idx]
    b = InlineKeyboardBuilder()
    if idx > 0:
        b.button(text="⬅️ Назад", callback_data=f"moment_{idx - 1}")
    if idx < len(MOMENTS) - 1:
        b.button(text="Вперед ➡️", callback_data=f"moment_{idx + 1}")
    b.button(text="🏠 Главное меню", callback_data="back_to_main")
    b.adjust(2, 1)
    await c.message.edit_text(text, reply_markup=b.as_markup())
    await c.answer()

@dp.callback_query(F.data == "back_to_main")
async def back_main(c: types.CallbackQuery):
    await c.message.edit_text(
        "Главное меню ❤️ Выбирай:",
        reply_markup=get_main_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data.startswith("date_"))
async def date_choice(c: types.CallbackQuery):
    choices = {
        "date_cinema": "🎬 Отличный выбор! Пойдем на классный фильм с попкорном и самыми удобными местами. Жду не дождусь! ❤️",
        "date_walk": "🌙 Ночная прогулка под звездами, теплая атмосфера и только мы вдвоем. Идеально! ✨",
        "date_dinner": "🍷 Романтический ужин, вкусная еда, красивые свечи и потрясающая компания. Жду тебя! 🍝",
        "date_secret": "🎁 Ого, выбор интригует! Это будет сюрприз, о котором ты точно не пожалеешь. Подсказка: бери хорошее настроение! 😉"
    }
    text = choices.get(c.data, "Идем?") + "\n\nНу что, согласна?"
    await c.message.edit_text(text, reply_markup=get_contact_keyboard())
    await c.answer()

async def handle(request):
    return web.Response(text="Bot is alive and running!")

async def self_ping():
    while True:
        await asyncio.sleep(840)
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(RENDER_URL) as resp:
                    logging.info(f"Ping: {resp.status}")
        except Exception as e:
            logging.error(f"Ping error: {e}")

app = web.Application()
app.router.add_get("/", handle)

async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(dp.start_polling(bot))
    asyncio.create_task(self_ping())

app.on_startup.append(on_startup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
