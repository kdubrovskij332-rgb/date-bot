import os
import logging
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import FSInputFile
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
    b.button(text="🎧 Музыкальный вайб ✨", callback_data="music_menu")
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

# Меню музыки
def get_music_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="🔥 Instasamka — Эверест", callback_data="play_everest")
    b.button(text="🎰 Dead Blonde — Казино", callback_data="play_casino")
    b.button(text="✨ Игнатов — Мое тело — убийца", callback_data="play_ignatov")
    b.button(text="⬅️ Назад в меню", callback_data="back_to_main")
    b.adjust(1)
    return b.as_markup()

def get_music_back_keyboard():
    b = InlineKeyboardBuilder()
    b.button(text="⬅️ Выбрать другую песню", callback_data="music_menu")
    b.button(text="⬅️ Назад в меню", callback_data="back_to_main")
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
        "Отличный выбор! Я знал, что тебе понравится. 💫\n\n"
        "Добро пожаловать в наш личный уголок. Выбирай, что тебе хочется посмотреть:",
        reply_markup=get_main_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "intro_no")
async def intro_no(c: types.CallbackQuery):
    await c.message.edit_text(
        "Нет, любимая, так не пойдёт! 😉 Слишком долго я это для тебя готовил, так что давай смотреть дальше! ❤️",
        reply_markup=get_intro_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "back_to_intro")
async def back_to_intro(c: types.CallbackQuery):
    await c.message.edit_text(
        "Привет, моя любимая! 🥰 Смотри, что я тут для тебя создал. "
        "Надеюсь, тебе понравится этот небольшой сюрприз!\n\nНу что, готовы двигаться дальше?",
        reply_markup=get_intro_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "menu_dates")
async def menu_dates(c: types.CallbackQuery):
    await c.message.edit_text(
        "Куда бы ты хотела отправиться на этот раз?",
        reply_markup=get_date_keyboard()
    )
    await c.answer()

@dp.callback_query(F.data == "sub_cinema")
async def sub_cinema(c: types.CallbackQuery):
    await c.message.edit_text("🎬 Какой жанр фильма выберем?", reply_markup=get_cinema_keyboard())
    await c.answer()

@dp.callback_query(F.data == "sub_dinner")
async def sub_dinner(c: types.CallbackQuery):
    await c.message.edit_text("🍷 Где устроим ужин?", reply_markup=get_dinner_keyboard())
    await c.answer()

@dp.callback_query(F.data == "sub_walk")
async def sub_walk(c: types.CallbackQuery):
    await c.message.edit_text("🌙 Где погуляем?", reply_markup=get_walk_keyboard())
    await c.answer()

# Музыкальное меню
@dp.callback_query(F.data == "music_menu")
async def music_menu_handler(c: types.CallbackQuery):
    await c.message.edit_text(
        "🎧 Выбери трек, который хочешь послушать прямо сейчас:",
        reply_markup=get_music_keyboard()
    )
    await c.answer()

# Отправка трека: Эверест
@dp.callback_query(F.data == "play_everest")
async def play_everest(c: types.CallbackQuery):
    try:
        audio_file = FSInputFile("everest.mp3")
        await bot.send_audio(
            chat_id=c.from_user.id,
            audio=audio_file,
            title="Эверест",
            performer="INSTASAMKA",
            caption="🔥 Instasamka — Эверест ⚡️"
        )
        await c.message.answer("Выбери еще что-нибудь из музыки:", reply_markup=get_music_back_keyboard())
    except Exception as e:
        logging.error(f"Error sending audio: {e}")
        await c.message.answer("Не удалось загрузить трек ❤️", reply_markup=get_music_back_keyboard())
    await c.answer()

# Отправка трека: Казино
@dp.callback_query(F.data == "play_casino")
async def play_casino(c: types.CallbackQuery):
    try:
        audio_file = FSInputFile("casino-deadBlonde.mp3")
        await bot.send_audio(
            chat_id=c.from_user.id,
            audio=audio_file,
            title="Казино",
            performer="Dead Blonde",
            caption="🎰 Dead Blonde — Казино 💫"
        )
        await c.message.answer("Выбери еще что-нибудь из музыки:", reply_markup=get_music_back_keyboard())
    except Exception as e:
        logging.error(f"Error sending audio: {e}")
        await c.message.answer("Не удалось загрузить трек ❤️", reply_markup=get_music_back_keyboard())
    await c.answer()

# Отправка трека: Мое тело — убийца
@dp.callback_query(F.data == "play_ignatov")
async def play_ignatov(c: types.CallbackQuery):
    try:
        audio_file = FSInputFile("Telo-ignat.mp3")
        await bot.send_audio(
            chat_id=c.from_user.id,
            audio=audio_file,
            title="Мое тело — убийца",
            performer="Игнатов",
            caption="✨ Игнатов — Мое тело — убийца ❤️"
        )
        await c.message.answer("Выбери еще что-нибудь из музыки:", reply_markup=get_music_back_keyboard())
    except Exception as e:
        logging.error(f"Error sending audio: {e}")
        await c.message.answer("Не удалось загрузить трек ❤️", reply_markup=get_music_back_keyboard())
    await c.answer()

# Навигация по моментам
@dp.callback_query(F.data.startswith("moment_"))
async def moment_nav(c: types.CallbackQuery):
    idx = int(c.data.split("_")[1])
    text = MOMENTS[idx]
    b = InlineKeyboardBuilder()
    if idx > 0:
        b.button(text="⬅️ Назад", callback_data=f"moment_{idx - 1}")
    if idx < len(MOMENTS) - 1:
        b.button(text="Вперед ➡️", callback_data=f"moment_{idx + 1}")
    b.button(text="⬅️ Назад в меню", callback_data="back_to_main")
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

@dp.callback_query(F.data.startswith("final_"))
async def final_choice(c: types.CallbackQuery):
    choice_type = c.data.replace("final_", "")
    
    descriptions = {
        "cinema_comedy": "🎬 Кино: Комедия",
        "cinema_horror": "🎬 Кино: Ужасы",
        "cinema_romance": "🎬 Кино: Мелодрама",
        "cinema_action": "🎬 Кино: Экшен / Боевик",
        "dinner_home": "🍷 Ужин: Дома (уютный вечер)",
        "dinner_restaurant": "🍷 Ужин: В ресторане",
        "dinner_picnic": "🍷 Ужин: Пикник",
        "dinner_roof": "🍷 Ужин: На крыше",
        "walk_krakow": "🌙 Прогулка: По ночному Кракову",
        "walk_nature": "🌙 Прогулка: В парке / лесу",
        "secret": "🎁 Секретный вариант-сюрприз"
    }
    
    result_text = descriptions.get(choice_type, "Свидание")
    
    try:
        await bot.send_message(
            MY_USER_ID,
            f"🚨 **Ура! Любимая сделала выбор свидания!**\n\nОна выбрала: *{result_text}* ❤️"
        )
    except Exception as e:
        logging.error(f"Не удалось отправить уведомление тебе: {e}")

    text = f"✨ Отличный выбор!\n\nТы выбрала: **{result_text}**.\n\nЯ уже получил твой выбор и жду не дождусь нашей встречи! ❤️"
    await c.message.edit_text(text, reply_markup=get_contact_keyboard())
    await c.answer()

async def handle_webhook(request: web.Request):
    data = await request.json()
    update = types.Update(**data)
    await dp.feed_update(bot, update)
    return web.Response()

async def self_ping():
    while True:
        await asyncio.sleep(840)
        try:
            async with aiohttp.ClientSession() as s:
                async with s.get(RENDER_URL) as resp:
                    logging.info(f"Ping: {resp.status}")
        except Exception as e:
            logging.error(f"Ping error: {e}")

async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    asyncio.create_task(self_ping())
    logging.info("Webhook is set successfully!")

app = web.Application()
app.router.add_post(WEBHOOK_PATH, handle_webhook)
app.router.add_get("/", lambda r: web.Response(text="Bot is running via webhooks!"))
app.on_startup.append(on_startup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
