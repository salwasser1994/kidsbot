import asyncio
import json
import random
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# === Настройка токена ===
API_TOKEN = "7174011610:AAGGjDniBS_D1HE_aGSxPA9M6mrGCZOeqNM"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === Очки сохраняем в файл ===
POINTS_FILE = Path("points.json")

def load_points():
    if POINTS_FILE.exists():
        with open(POINTS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_points():
    with open(POINTS_FILE, "w", encoding="utf-8") as f:
        json.dump(points, f, ensure_ascii=False, indent=2)

points = load_points()

# === ДАННЫЕ ПРОФИЛЕЙ ===
profiles = {
    "Алиса": {
        "birthday": "2016-06-19",
        "greetings": "Привет, волшебница Алиса ✨!",
        "facts": [
            "Алиса умеет очень быстро собирать пазлы 🧩",
            "Алиса любит котиков 🐱",
            "Алиса знает, что слоны боятся мышей 🐘🐭"
        ],
        "jokes": [
            "Почему книга пошла в больницу? Потому что у неё сломалась обложка 📚😂",
            "Кто всегда идёт, но никогда не приходит? Завтра ⏳",
            "Почему карандаш грустный? Потому что у него нет точилки ✏️😢"
        ],
        "tasks": [
            "Алиса, попробуй 10 секунд постоять на одной ножке 🦶",
            "Сможешь назвать 5 фруктов за 15 секунд? 🍎🍌🍇🍊🍓",
            "Придумай смешное слово из букв Б, К и Л!"
        ]
    },
    "Руслан": {
        "birthday": "2014-11-04",
        "greetings": "Здравствуй, исследователь Руслан 🚀!",
        "facts": [
            "Руслан — чемпион по скоростному бегу на месте 🏃",
            "Руслан обожает динозавров 🦖",
            "Руслан знает, что у акулы более 300 зубов 🦈"
        ],
        "jokes": [
            "Почему компьютер пошёл в школу? Чтобы стать умнее 🤓",
            "Какая рыба не умеет плавать? Жареная 🐟",
            "Почему велосипед упал? Потому что он устал 🚲😂"
        ],
        "tasks": [
            "Руслан, попробуй придумать рифму к слову 'школа' 🎓",
            "Сможешь за 20 секунд назвать 5 животных? 🐶🐱🐰🐯🐴",
            "Попрыгай 7 раз на месте, как кенгуру 🦘"
        ]
    }
}

# === Общие даты ===
common_dates = {
    "new_year": "2026-01-01",
    "summer_holidays": "2026-06-01"
}

# === user_id → имя ребёнка (замени на реальные id) ===
user_to_name = {
   7719485802: "Алиса",
    987654321: "Руслан"
}

# === Вспомогательные функции ===
def days_until(date_str: str) -> int:
    today = datetime.today().date()
    target = datetime.strptime(date_str, "%Y-%m-%d").date()
    delta = (target - today).days
    return delta if delta >= 0 else (target.replace(year=today.year + 1) - today).days

def get_points(user_id: int) -> int:
    return points.get(str(user_id), 0)

def add_point(user_id: int, value: int = 1):
    points[str(user_id)] = get_points(user_id) + value
    save_points()

def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Игры и задания", callback_data="tasks")],
        [InlineKeyboardButton(text="📖 Интересный факт", callback_data="fact")],
        [InlineKeyboardButton(text="😂 Анекдот", callback_data="joke")],
        [InlineKeyboardButton(text="📅 Сколько дней до...", callback_data="days")],
        [InlineKeyboardButton(text="🏆 Мои очки", callback_data="points")],
        [InlineKeyboardButton(text="🙋 Кто я", callback_data="whoami")]
    ])

def days_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎂 День рождения Алисы", callback_data="days_alice")],
        [InlineKeyboardButton(text="🎂 День рождения Руслана", callback_data="days_ruslan")],
        [InlineKeyboardButton(text="🎄 Новый год", callback_data="days_newyear")],
        [InlineKeyboardButton(text="☀️ Каникулы", callback_data="days_holidays")]
    ])

# === Обработчики ===
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    name = user_to_name.get(message.from_user.id)
    if name:
        profile = profiles[name]
        await message.answer(
            f"{profile['greetings']}\nЧто хочешь сделать?",
            reply_markup=main_menu()
        )
    else:
        await message.answer("Привет! Тебя я пока не знаю 🤔")

@dp.callback_query(F.data == "whoami")
async def who_am_i(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        profile = profiles[name]
        text = (
            f"Ты — {name} 🎉\n"
            f"📅 День рождения: {profile['birthday']}\n"
            f"🎯 Очков: {get_points(callback.from_user.id)}\n"
            f"💡 Например: {profile['facts'][0]}"
        )
        await callback.message.answer(text)
    await callback.answer()

@dp.callback_query(F.data == "fact")
async def fact(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        fact = random.choice(profiles[name]["facts"])
        await callback.message.answer(fact)
    await callback.answer()

@dp.callback_query(F.data == "joke")
async def joke(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        joke = random.choice(profiles[name]["jokes"])
        await callback.message.answer(joke)
    await callback.answer()

@dp.callback_query(F.data == "tasks")
async def task(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        task = random.choice(profiles[name]["tasks"])
        add_point(callback.from_user.id, 1)
        await callback.message.answer(task)
        await callback.message.answer(
            f"Ты получил 1 очко! 🎯 Всего очков: {get_points(callback.from_user.id)}"
        )
    await callback.answer()

@dp.callback_query(F.data == "points")
async def points_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        f"У тебя {get_points(callback.from_user.id)} очков 🎯"
    )
    await callback.answer()

@dp.callback_query(F.data == "days")
async def days(callback: types.CallbackQuery):
    await callback.message.answer("Выбери событие:", reply_markup=days_menu())
    await callback.answer()

@dp.callback_query(F.data.startswith("days_"))
async def days_event(callback: types.CallbackQuery):
    data = callback.data

    if data == "days_alice":
        target = profiles["Алиса"]["birthday"]
        text = f"До дня рождения Алисы 🎂 осталось {days_until(target)} дней!"
    elif data == "days_ruslan":
        target = profiles["Руслан"]["birthday"]
        text = f"До дня рождения Руслана 🎂 осталось {days_until(target)} дней!"
    elif data == "days_newyear":
        target = common_dates["new_year"]
        text = f"До Нового года 🎄 осталось {days_until(target)} дней!"
    elif data == "days_holidays":
        target = common_dates["summer_holidays"]
        text = f"До летних каникул ☀️ осталось {days_until(target)} дней!"

    await callback.message.answer(text)
    await callback.answer()

# === Запуск ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
