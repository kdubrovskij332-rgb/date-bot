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

# Замени на адрес твоего веб-сервиса на Render (без слэша на конце)
RENDER_URL = "https://date-bot-3aj8.onrender.com"

# Разрешенные ID: её ID и твой ID
ALLOWED_USER_IDS = [
    1067015608, # ID твоей девушки
    1029773942  # Твой ID
]

# Список ваших совместных фотографий
PHOTOS = [
    {
        "url": "https://images.unsplash.com/photo-1516589178581-6cd7833ae3b2?q=80&w=1000&auto=format&fit=crop",
        "caption": "✨ Наши моменты (1 из 5)\n\nЛюбимая, эта неделя особенная, совсем как ты. Спасибо за то, что ты у меня есть! 🥰"
    },
    {
        "url": "https://images.unsplash.com/photo-1518199266791-5375a83190b7?q=80&w=1000&auto=format&fit=crop",
        "caption": "✨ Наши моменты (2 из 5)\n\nКаждый день с тобой — это отдельное маленькое приключение. ❤️"
    },
    {
        "url": "https://images.unsplash.com/photo-1522748987366-3d2f23604f76?q=80&w=1000&auto=format&fit=crop",
        "caption": "✨ Наши моменты (3 из 5)\n\nДаже в самый пасмурный день рядом с тобой тепло и уютно. ✨"
    },
    {
        "url": "https://images.unsplash.com/photo-1494774157365-9e04c6720e47?q=80&w=1000&auto=format&fit=crop",
        "caption": "✨ Наши моменты (4 из 5)\n\nКрасотка моя! Самые лучшие моменты только с тобой. 💫"
    },
    {
        "url": "https://images.unsplash.com/photo-1529156069898-49953e39b3ac?q=80&w=1000&auto=format&fit=crop",
        "caption": "✨ Наши моменты (5 из 5)\n\nЧуть позже добавлю что-то еще... А пока просто знай, как сильно я тебя люблю! 🥰❤️"
    }
]

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

def is_allowed(user_id: int) -> bool:
    return user_id in ALLOWED_USER_IDS

def get_main_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="💌 Выбрать свидание", callback_data="menu_dates")
    builder.button(text="📸 Наши моменты и сюрприз", callback_data="photo_0")
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
        "Привет, моя родная! 🥰 Добро пожаловать в наш личный уголок. "
        "Выбирай, что тебе хочется посмотреть:",
        reply_markup=get_main_keyboard()
    )

@dp.callback_query(F.data == "menu_dates")
async def process_menu_dates(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Куда бы ты хотела отправиться на этот раз?",
        reply_markup=get_date_keyboard()
    )
    await callback.answer()

@dp.callback_query(F.data.startswith("photo_"))
async def process_photo_navigation(callback: types.CallbackQuery):
    index = int(callback.data.split("_")[1])
    photo_data = PHOTOS[index]
    
    builder = InlineKeyboardBuilder()
    
    if index > 0:
        builder.button(text="⬅️ Назад", callback_data=f"photo_{index - 1}")
    if index < len(PHOTOS) - 1:
        builder.button(text="Вперед ➡️", callback_data=f"photo_{index + 1}")
        
    builder.button(text="🏠 Главное меню", callback_data="back_to_main")
    builder.adjust(2, 1)
    
    await callback.message.answer_photo(
        photo=photo_data["url"],
        caption=photo_data["caption"],
        reply_markup=builder.as_markup()
    )
    try:
        await callback.message.delete()
    except:
        pass
    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def process_back(callback: types.CallbackQuery):
    await callback.message.answer(
        "Главное меню ❤️ Выбирай:",
        reply_markup=get_main_keyboard()
    )
    try:
        await callback.message.delete()
    except:
        pass
    await callback.answer()

@dp.callback_query(F.data.startswith("date_"))
async def process_date_choice(callback: types.CallbackQuery):
    choices = {
        "date_cinema": "🎬 Отличный выбор! Пойдем на классный фильм с попкорном и самыми удобными местами. Жду не дождусь! ❤️",
        "date_walk": "🌙 Ночная прогулка под звездами, теплая атмосфера и только мы вдвоем. Идеально! ✨",
        "date_dinner": "🍷 Романтический ужин, вкусная еда, красивые свечи и потрясающая компания. Жду тебя! 🍝",
        "date_secret": "🎁 Ого, выбор интригует! Это будет сюрприз, о котором ты точно не пожалеешь. Подсказка: бери хорошее настроение! 😉"
    }
    
    text = choices.get(callback.data, "Идем?") + "\n\nНу что, согласна?"
    await callback.message.edit_text(text, reply_markup=get_contact_keyboard())
    await callback.answer()

async def handle(request):
    return web.Response(text="Bot is alive and running!")

# Фоновая задача, которая пингует сайт каждые 14 минут, чтобы он не засыпал
async def self_ping():
    while True:
        await asyncio.sleep(840) # 14 минут
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(RENDER_URL) as resp:
                    logging.info(f"Self-ping status: {resp.status}")
        except Exception as e:
            logging.error(f"Self-ping error: {e}")

app = web.Application()
app.router.add_get("/", handle)

async def on_startup(app):
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(dp.start_polling(bot))
    asyncio.create_task(self_ping()) # Запускаем анти-сон

app.on_startup.append(on_startup)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    web.run_app(app, host="0.0.0.0", port=port)
