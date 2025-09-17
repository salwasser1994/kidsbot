# bot.py
import asyncio
import json
import random
from datetime import datetime
from pathlib import Path

from aiogram import Bot, Dispatcher, types, F
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command

# === Настройка токена ===
API_TOKEN = "7174011610:AAGGjDniBS_D1HE_aGSxPA9M6mrGCZOeqNM"  # <- замените на реальный токен
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

# === Временные игры (в памяти) ===
# Для "угадай число" храним загаданное число для каждого пользователя
guess_number_games: dict[str, int] = {}
# Для викторины можно хранить активный вопрос id (не обязательно сейчас)
active_quiz: dict[str, int] = {}

# === Профили ===
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
        "birthday": "2014-10-04",
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
# Пример:
# user_to_name = {
#    7719485802: "Алиса",
#     222222222: "Руслан"
# }
user_to_name: dict[int, str] = {
    7719485802: "Алиса",
    987654321: "Руслан"
}

# === Вспомогательные ===
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

# === Клавиатуры ===
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Игры и задания", callback_data="tasks")],
        [InlineKeyboardButton(text="🧠 Викторина", callback_data="quiz")],
        [InlineKeyboardButton(text="🎮 Угадай число", callback_data="guessnum_start")],
        [InlineKeyboardButton(text="✊✋✌️ Камень-ножницы-бумага", callback_data="rps_start")],
        [InlineKeyboardButton(text="🎁 Сюрприз", callback_data="surprise")],
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
        [InlineKeyboardButton(text="☀️ Каникулы", callback_data="days_holidays")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
    ])

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
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
        await message.answer(
            "Привет! Кажется, я пока не знаю тебя. Попроси взрослого добавить твой user_id в конфигурацию бота."
        )

@dp.callback_query(F.data == "main_menu")
async def go_main(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        await callback.message.answer("Главное меню:", reply_markup=main_menu())
    else:
        await callback.message.answer("Я тебя пока не знаю 😕")
    await callback.answer()

# === Кто я ===
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
        await callback.message.answer(text, reply_markup=back_menu())
    else:
        await callback.message.answer("Я тебя пока не знаю 😕", reply_markup=back_menu())
    await callback.answer()

# === Факт ===
@dp.callback_query(F.data == "fact")
async def fact(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        fact_text = random.choice(profiles[name]["facts"])
        await callback.message.answer(fact_text, reply_markup=back_menu())
    else:
        await callback.message.answer("Я тебя пока не знаю 😕", reply_markup=back_menu())
    await callback.answer()

# === Анекдот ===
@dp.callback_query(F.data == "joke")
async def joke(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        joke_text = random.choice(profiles[name]["jokes"])
        await callback.message.answer(joke_text, reply_markup=back_menu())
    else:
        await callback.message.answer("Я тебя пока не знаю 😕", reply_markup=back_menu())
    await callback.answer()

# === Игры и задания ===
@dp.callback_query(F.data == "tasks")
async def task(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if name:
        task_text = random.choice(profiles[name]["tasks"])
        add_point(callback.from_user.id, 1)
        await callback.message.answer(task_text, reply_markup=back_menu())
        await callback.message.answer(
            f"Ты получил 1 очко! 🎯 Всего очков: {get_points(callback.from_user.id)}",
            reply_markup=back_menu()
        )
    else:
        await callback.message.answer("Я тебя пока не знаю 😕", reply_markup=back_menu())
    await callback.answer()

# === Викторина ===
quiz_questions = [
    {"q": "Сколько ног у паука?", "options": ["6", "8", "10"], "answer_index": 1},
    {"q": "Какого цвета банан?", "options": ["Красный", "Жёлтый", "Синий"], "answer_index": 1},
    {"q": "Кто громче всех кукарекает?", "options": ["Курица", "Петух", "Утка"], "answer_index": 1},
]

@dp.callback_query(F.data == "quiz")
async def quiz_start(callback: types.CallbackQuery):
    qid = random.randrange(len(quiz_questions))
    active_quiz[str(callback.from_user.id)] = qid
    q = quiz_questions[qid]
    buttons = []
    for idx, opt in enumerate(q["options"]):
        buttons.append([InlineKeyboardButton(text=opt, callback_data=f"quiz:{qid}:{idx}")])
    buttons.append([InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")])
    kb = InlineKeyboardMarkup(inline_keyboard=buttons)
    await callback.message.answer(q["q"], reply_markup=kb)
    await callback.answer()

@dp.callback_query(F.data.startswith("quiz:"))
async def quiz_answer(callback: types.CallbackQuery):
    data = callback.data.split(":")
    if len(data) != 3:
        await callback.answer()
        return
    qid = int(data[1]); chosen_idx = int(data[2])
    q = quiz_questions[qid]
    correct_idx = q["answer_index"]
    if chosen_idx == correct_idx:
        add_point(callback.from_user.id, 2)
        await callback.message.answer("Правильно! 🎉 +2 очка!", reply_markup=back_menu())
    else:
        correct_text = q["options"][correct_idx]
        await callback.message.answer(f"Неправильно — правильный ответ: {correct_text}", reply_markup=back_menu())
    await callback.answer()

# === Угадай число ===
def make_guessnum_kb():
    rows = []
    # делаем кнопки 1..10 (по 5 в ряд)
    for i in range(1, 11):
        rows.append(InlineKeyboardButton(text=str(i), callback_data=f"guessnum_choice:{i}"))
    # InlineKeyboardMarkup требует список строк -> разобьём по 5
    keyboard = InlineKeyboardMarkup(row_width=5)
    keyboard.add(*[InlineKeyboardButton(text=str(i), callback_data=f"guessnum_choice:{i}") for i in range(1, 11)])
    # добавим назад
    keyboard.add(InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu"))
    return keyboard

@dp.callback_query(F.data == "guessnum_start")
async def guessnum_start(callback: types.CallbackQuery):
    # загадываем число 1..10
    secret = random.randint(1, 10)
    guess_number_games[str(callback.from_user.id)] = secret
    await callback.message.answer("Я загадал число от 1 до 10. Попробуй угадать!", reply_markup=make_guessnum_kb())
    await callback.answer()

@dp.callback_query(F.data.startswith("guessnum_choice:"))
async def guessnum_choice(callback: types.CallbackQuery):
    user_id = str(callback.from_user.id)
    if user_id not in guess_number_games:
        await callback.message.answer("Сначала нажми 'Угадай число' чтобы начать игру.", reply_markup=back_menu())
        await callback.answer()
        return
    try:
        chosen = int(callback.data.split(":")[1])
    except Exception:
        await callback.answer()
        return
    secret = guess_number_games.pop(user_id, None)
    if secret is None:
        await callback.message.answer("Игра не найдена. Нажми 'Угадай число' чтобы начать.", reply_markup=back_menu())
    else:
        if chosen == secret:
            add_point(callback.from_user.id, 3)
            await callback.message.answer(f"Ура! Ты угадал(а) — это {secret}! 🎉 +3 очка!", reply_markup=back_menu())
        else:
            await callback.message.answer(f"Повезёт в следующий раз — я загадал(а) {secret}.", reply_markup=back_menu())
    await callback.answer()

# === Камень-ножницы-бумага ===
def rps_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✊ Камень", callback_data="rps:rock"),
         InlineKeyboardButton(text="✋ Бумага", callback_data="rps:paper"),
         InlineKeyboardButton(text="✌️ Ножницы", callback_data="rps:scissors")],
        [InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")]
    ])

@dp.callback_query(F.data == "rps_start")
async def rps_start(callback: types.CallbackQuery):
    await callback.message.answer("Камень, ножницы, бумага! Выбирай:", reply_markup=rps_kb())
    await callback.answer()

@dp.callback_query(F.data.startswith("rps:"))
async def rps_play(callback: types.CallbackQuery):
    try:
        user_choice = callback.data.split(":")[1]
    except Exception:
        await callback.answer()
        return
    bot_choice = random.choice(["rock", "paper", "scissors"])
    # определяем победителя
    outcome = None  # "win", "lose", "draw"
    if user_choice == bot_choice:
        outcome = "draw"
    elif (user_choice == "rock" and bot_choice == "scissors") or \
         (user_choice == "paper" and bot_choice == "rock") or \
         (user_choice == "scissors" and bot_choice == "paper"):
        outcome = "win"
    else:
        outcome = "lose"

    emoji_name = {"rock": "✊ Камень", "paper": "✋ Бумага", "scissors": "✌️ Ножницы"}

    if outcome == "win":
        add_point(callback.from_user.id, 2)
        await callback.message.answer(f"Я выбрал(а) {emoji_name[bot_choice]}. Ты победил(а)! 🎉 +2 очка!", reply_markup=back_menu())
    elif outcome == "lose":
        await callback.message.answer(f"Я выбрал(а) {emoji_name[bot_choice]}. К сожалению, ты проиграл(а). Попробуй ещё! 😊", reply_markup=back_menu())
    else:
        await callback.message.answer(f"Мы оба выбрали {emoji_name[bot_choice]}. Ничья! 🤝", reply_markup=back_menu())
    await callback.answer()

# === Сюрприз ===
@dp.callback_query(F.data == "surprise")
async def surprise(callback: types.CallbackQuery):
    name = user_to_name.get(callback.from_user.id)
    if not name:
        await callback.message.answer("Я тебя пока не знаю 😕", reply_markup=back_menu())
        await callback.answer()
        return

    choice = random.choice(["fact", "joke", "task", "mini_quiz"])
    if choice == "fact":
        text = random.choice(profiles[name]["facts"])
        await callback.message.answer("🎉 Сюрприз — факт:\n" + text, reply_markup=back_menu())
    elif choice == "joke":
        text = random.choice(profiles[name]["jokes"])
        await callback.message.answer("🎉 Сюрприз — шутка:\n" + text, reply_markup=back_menu())
    elif choice == "task":
        text = random.choice(profiles[name]["tasks"])
        add_point(callback.from_user.id, 1)
        await callback.message.answer("🎉 Сюрприз — задание:\n" + text, reply_markup=back_menu())
        await callback.message.answer(f"Ты получил(а) 1 очко! 🎯 Всего: {get_points(callback.from_user.id)}", reply_markup=back_menu())
    elif choice == "mini_quiz":
        # быстрая захардкоженная мини-викторина (1 вопрос)
        q = random.choice(quiz_questions)
        # используем опции как кнопки, но пометим callback как quickquiz so it won't interfere
        buttons = []
        for idx, opt in enumerate(q["options"]):
            buttons.append([InlineKeyboardButton(text=opt, callback_data=f"quickquiz:{q['q']}:{idx}:{q['answer_index']}")])
        buttons.append([InlineKeyboardButton(text="🔙 Назад в меню", callback_data="main_menu")])
        kb = InlineKeyboardMarkup(inline_keyboard=buttons)
        await callback.message.answer("🎉 Сюрприз — мини-викторина:\n" + q["q"], reply_markup=kb)
    await callback.answer()

@dp.callback_query(F.data.startswith("quickquiz:"))
async def quickquiz_answer(callback: types.CallbackQuery):
    # формат quickquiz:question_text:chosen_idx:correct_idx
    parts = callback.data.split(":", 3)
    if len(parts) < 4:
        await callback.answer()
        return
    _, q_text, chosen_idx, correct_idx = parts
    chosen_idx = int(chosen_idx); correct_idx = int(correct_idx)
    if chosen_idx == correct_idx:
        add_point(callback.from_user.id, 2)
        await callback.message.answer("Правильно! 🎉 +2 очка!", reply_markup=back_menu())
    else:
        await callback.message.answer("Неправильно — в другой раз получится! 😊", reply_markup=back_menu())
    await callback.answer()

# === Очки ===
@dp.callback_query(F.data == "points")
async def points_handler(callback: types.CallbackQuery):
    await callback.message.answer(
        f"У тебя {get_points(callback.from_user.id)} очков 🎯",
        reply_markup=back_menu()
    )
    await callback.answer()

# === Дни ===
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
    else:
        text = "Неизвестное событие."
    await callback.message.answer(text, reply_markup=back_menu())
    await callback.answer()

# === Запуск ===
async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
