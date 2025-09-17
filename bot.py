import asyncio
import random
from datetime import datetime
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup

# === ТОКЕН БОТА ===
API_TOKEN = "7174011610:AAGGjDniBS_D1HE_aGSxPA9M6mrGCZOeqNM"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# === ДЕТИ (user_id + данные) ===
users = {
    "Руслан": {"id": 7894501725, "birthday": "2014-10-04", "points": 0},
    "Алиса": {"id": 7719485802, "birthday": "2016-06-19", "points": 0},
    "Томас": {"id": 5205381793, "birthday": "1994-04-27", "points": 0},
}

# === ВИКТОРИНА (50 случайных вопросов) ===
quiz_questions = [
    ("Столица Франции?", ["Париж", "Лондон", "Берлин", "Рим"], "Париж"),
    ("Сколько будет 2+2?", ["3", "4", "5", "6"], "4"),
    ("Самая длинная река в мире?", ["Амазонка", "Нил", "Волга", "Янцзы"], "Нил"),
    ("Как называется спутник Земли?", ["Марс", "Луна", "Венера", "Сатурн"], "Луна"),
    ("Кто написал 'Войну и мир'?", ["Толстой", "Пушкин", "Гоголь", "Чехов"], "Толстой"),
    ("Сколько ног у паука?", ["6", "8", "10", "12"], "8"),
    ("Какая планета ближе всего к Солнцу?", ["Меркурий", "Венера", "Марс", "Юпитер"], "Меркурий"),
    ("Какой цвет у моркови?", ["Красный", "Оранжевый", "Зелёный", "Фиолетовый"], "Оранжевый"),
    ("Сколько букв в русском алфавите?", ["32", "33", "34", "31"], "33"),
    ("Кто изобрёл лампу?", ["Эдисон", "Ньютон", "Тесла", "Дарвин"], "Эдисон"),
] * 5  # 50 вопросов

# Уже заданные вопросы по каждому юзеру
asked_questions = {}

# === АНЕКДОТЫ ===
jokes = [
    "— Папа, а почему солнце встаёт на востоке?\n— Один раз опоздало и его уволили!",
    "Учитель: Вовочка, почему ты опоздал?\nВовочка: А вы сами говорили — лучше поздно, чем никогда!",
    "Встречаются два крокодила: — Ты где был? — В Египте. — Ну и как там? — Да нормально, только египтяне всё время бегают и кричат: 'Крокодил! Крокодил!'"
]

# === СКАЗКИ ===
fairytales = [
    "Жил-был колобок. Он убежал от бабушки, дедушки, но встретил лису... 🦊",
    "В тридевятом царстве жила-была Василиса Прекрасная... 👸",
    "Жил-был маленький дракончик. Он боялся летать, но однажды... 🐉"
]

# === ЗАГАДКИ ===
riddles = [
    ("Зимой и летом одним цветом. Что это?", "Ёлка"),
    ("Без окон, без дверей — полна горница людей. Что это?", "Огурец"),
    ("Висит груша — нельзя скушать. Что это?", "Лампочка"),
]

# === ЖИВОТНЫЕ ===
animals = ["Кошка 🐱", "Собака 🐶", "Заяц 🐇", "Лев 🦁", "Слон 🐘", "Медведь 🐻", "Пингвин 🐧", "Крокодил 🐊"]

# Хранение текущих игр
current_games = {}

# === МЕНЮ ===
def main_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎲 Угадай число", callback_data="guessnum")],
        [InlineKeyboardButton(text="📖 Сказка", callback_data="fairytale")],
        [InlineKeyboardButton(text="😆 Анекдот", callback_data="joke")],
        [InlineKeyboardButton(text="❓ Загадка", callback_data="riddle")],
        [InlineKeyboardButton(text="🧩 Викторина", callback_data="quiz")],
        [InlineKeyboardButton(text="✊✌️✋ Камень-Ножницы-Бумага", callback_data="rps")],
        [InlineKeyboardButton(text="🐾 Угадай животное", callback_data="animal")],
        [InlineKeyboardButton(text="➕➖✖️ Математический челлендж", callback_data="math")],
        [InlineKeyboardButton(text="🏆 Мои очки", callback_data="points")],
        [InlineKeyboardButton(text="👤 Кто я", callback_data="whoami")],
        [InlineKeyboardButton(text="📅 Сколько дней до ДР?", callback_data="birthday")],
    ])
    return kb

def back_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад в главное меню", callback_data="back")]
    ])

# === Определение ребёнка по user_id ===
def get_child(user_id: int):
    for name, data in users.items():
        if data["id"] == user_id:
            return name
    return None

# === СТАРТ ===
@dp.message(F.text == "/start")
async def start(message: Message):
    child = get_child(message.from_user.id)
    if child:
        await message.answer(f"Привет, {child}! 👋\nВыбери, что будем делать:", reply_markup=main_menu())
    else:
        await message.answer("Привет! 🚫 Ты не зарегистрирован для игры в этом боте.")

# === НАЗАД ===
@dp.callback_query(F.data == "back")
async def go_back(callback: CallbackQuery):
    await callback.message.edit_text("Главное меню:", reply_markup=main_menu())

# === АНЕКДОТ ===
@dp.callback_query(F.data == "joke")
async def send_joke(callback: CallbackQuery):
    await callback.message.edit_text(random.choice(jokes), reply_markup=back_menu())

# === СКАЗКА ===
@dp.callback_query(F.data == "fairytale")
async def send_fairytale(callback: CallbackQuery):
    await callback.message.edit_text(random.choice(fairytales), reply_markup=back_menu())

# === ЗАГАДКА ===
@dp.callback_query(F.data == "riddle")
async def send_riddle(callback: CallbackQuery):
    question, answer = random.choice(riddles)
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Показать ответ", callback_data=f"riddle_answer:{answer}")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])
    await callback.message.edit_text(question, reply_markup=kb)

@dp.callback_query(F.data.startswith("riddle_answer"))
async def riddle_answer(callback: CallbackQuery):
    await callback.message.edit_text(f"Ответ: {callback.data.split(':')[1]}", reply_markup=back_menu())

# === УГАДАЙ ЧИСЛО ===
@dp.callback_query(F.data == "guessnum")
async def guessnum_start(callback: CallbackQuery):
    number = random.randint(1, 10)
    uid = callback.from_user.id
    current_games.setdefault(uid, {})
    current_games[uid]['guessnum'] = number
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(i), callback_data=f"guess:{i}") for i in range(1, 6)],
        [InlineKeyboardButton(text=str(i), callback_data=f"guess:{i}") for i in range(6, 11)],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])
    await callback.message.edit_text("Я загадал число от 1 до 10. Попробуй угадать!", reply_markup=kb)

@dp.callback_query(F.data.startswith("guess:"))
async def guessnum_check(callback: CallbackQuery):
    uid = callback.from_user.id
    number = current_games.get(uid, {}).get("guessnum", None)
    choice = int(callback.data.split(":")[1])
    if number is None:
        # нет активной игры — предложим начать заново
        await callback.message.edit_text("Игра не запущена. Нажми снова 'Угадай число'.", reply_markup=main_menu())
        return

    if choice == number:
        await callback.message.edit_text(f"🎉 Молодец! Это {number}!", reply_markup=back_menu())
        # очищаем игру
        current_games[uid].pop('guessnum', None)
    else:
        # повторяем тот же вопрос и клавиатуру
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(i), callback_data=f"guess:{i}") for i in range(1, 6)],
            [InlineKeyboardButton(text=str(i), callback_data=f"guess:{i}") for i in range(6, 11)],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ])
        await callback.message.edit_text(f"Нет 😅 Это не {choice}. Подумай ещё раз!", reply_markup=kb)

# === ВИКТОРИНА ===
@dp.callback_query(F.data == "quiz")
async def quiz_start(callback: CallbackQuery):
    user_id = callback.from_user.id
    asked_questions[user_id] = []
    current_games.setdefault(user_id, {})
    await ask_question(callback.message, user_id)

async def ask_question(message: Message, user_id: int):
    available = [q for q in quiz_questions if q not in asked_questions[user_id]]
    if not available:
        await message.edit_text("Ты ответил на все вопросы! 🎉", reply_markup=back_menu())
        # очистим текущее состояние викторины
        current_games.get(user_id, {}).pop('quiz', None)
        return
    question, options, correct = random.choice(available)
    # сохраняем текущую вопрос-строку в current_games, но не помечаем как отвеченный
    current_games.setdefault(user_id, {})
    current_games[user_id]['quiz'] = (question, options, correct)

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"quiz_answer:{opt}:{correct}")]
                         for opt in options] +
                        [[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]]
    )
    await message.edit_text(f"❓ {question}", reply_markup=kb)

@dp.callback_query(F.data.startswith("quiz_answer"))
async def quiz_answer(callback: CallbackQuery):
    parts = callback.data.split(":")
    # формат: quiz_answer:{opt}:{correct}
    if len(parts) < 3:
        await callback.answer("Ошибка данных.")
        return
    _, answer, correct = parts
    uid = callback.from_user.id
    child = get_child(uid)

    # берём текущую викторину из состояния (для повторного показа при ошибке)
    qdata = current_games.get(uid, {}).get('quiz', None)
    if qdata is None:
        await callback.message.edit_text("Вопрос недоступен. Нажми 'Викторина' чтобы начать заново.", reply_markup=main_menu())
        return

    question, options, correct_saved = qdata

    if answer == correct:
        # правильный — начисляем очки, помечаем вопрос как заданный и даём следующий
        if child:
            users[child]["points"] += 1
        # помечаем вопрос как заданный (чтобы не повторялся)
        asked_questions.setdefault(uid, []).append(qdata)
        # удаляем текущее состояние викторины
        current_games[uid].pop('quiz', None)
        await ask_question(callback.message, uid)
    else:
        # неправильный — не заканчиваем, предлагаем подумать ещё раз и показываем те же варианты
        kb = InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"quiz_answer:{opt}:{correct_saved}")]
                             for opt in options] +
                            [[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]]
        )
        name_part = f", {child}" if child else ""
        await callback.message.edit_text(f"❌ Неправильно{name_part}! Подумай ещё раз.", reply_markup=kb)

# === КАМЕНЬ-НОЖНИЦЫ-БУМАГА ===
@dp.callback_query(F.data == "rps")
async def rps_start(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✊ Камень", callback_data="rps:камень"),
         InlineKeyboardButton(text="✌️ Ножницы", callback_data="rps:ножницы"),
         InlineKeyboardButton(text="✋ Бумага", callback_data="rps:бумага")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
    ])
    await callback.message.edit_text("Выбирай! ✊✌️✋", reply_markup=kb)

@dp.callback_query(F.data.startswith("rps:"))
async def rps_play(callback: CallbackQuery):
    player = callback.data.split(":")[1]
    bot_choice = random.choice(["камень", "ножницы", "бумага"])
    if player == bot_choice:
        result = "Ничья!"
    elif (player == "камень" and bot_choice == "ножницы") or \
         (player == "ножницы" and bot_choice == "бумага") or \
         (player == "бумага" and bot_choice == "камень"):
        result = "Ты выиграл 🎉"
    else:
        result = "Я выиграл 😎"
    await callback.message.edit_text(f"Ты выбрал {player}, я выбрал {bot_choice}. {result}", reply_markup=back_menu())

# === УГАДАЙ ЖИВОТНОЕ ===
@dp.callback_query(F.data == "animal")
async def animal_start(callback: CallbackQuery):
    correct = random.choice(animals)
    uid = callback.from_user.id
    current_games.setdefault(uid, {})
    current_games[uid]['animal'] = {}
    options = random.sample(animals, 3)
    if correct not in options:
        options[0] = correct
    random.shuffle(options)
    current_games[uid]['animal']['correct'] = correct
    current_games[uid]['animal']['options'] = options

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=a, callback_data=f"animal:{a}:{correct}")] for a in options
    ] + [[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]])
    await callback.message.edit_text("Какое животное я загадал? 🐾", reply_markup=kb)

@dp.callback_query(F.data.startswith("animal:"))
async def animal_check(callback: CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("Ошибка данных.")
        return
    _, choice, correct = parts
    uid = callback.from_user.id
    state = current_games.get(uid, {}).get('animal', None)
    if state is None:
        await callback.message.edit_text("Игра не запущена. Нажми 'Угадай животное' чтобы начать.", reply_markup=main_menu())
        return

    if choice == correct:
        await callback.message.edit_text(f"🎉 Верно! Это {correct}", reply_markup=back_menu())
        current_games[uid].pop('animal', None)
    else:
        # показываем ту же клавиатуру с теми же опциями
        options = state['options']
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=a, callback_data=f"animal:{a}:{state['correct']}")] for a in options
        ] + [[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]])
        await callback.message.edit_text("❌ Нет! Подумай ещё раз.", reply_markup=kb)

# === МАТЕМАТИЧЕСКИЙ ЧЕЛЛЕНДЖ ===
@dp.callback_query(F.data == "math")
async def math_start(callback: CallbackQuery):
    await send_math_task(callback.message, callback.from_user.id)

async def send_math_task(message: Message, user_id: int):
    a, b = random.randint(1, 10), random.randint(1, 10)
    op = random.choice(["+", "-", "×"])
    if op == "+":
        correct = a + b
    elif op == "-":
        correct = a - b
    else:
        correct = a * b
    options = [correct, correct + 1, correct - 1, random.randint(1, 20)]
    random.shuffle(options)
    # сохраняем задачу в состоянии пользователя
    current_games.setdefault(user_id, {})
    current_games[user_id]['math'] = {"a": a, "b": b, "op": op, "correct": correct, "options": options}

    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=str(opt), callback_data=f"math_answer:{opt}:{correct}")] for opt in options
    ] + [[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]])
    await message.edit_text(f"Сколько будет {a} {op} {b}?", reply_markup=kb)

@dp.callback_query(F.data.startswith("math_answer"))
async def math_answer(callback: CallbackQuery):
    parts = callback.data.split(":")
    if len(parts) < 3:
        await callback.answer("Ошибка данных.")
        return
    _, answer, correct_str = parts
    uid = callback.from_user.id
    child = get_child(uid)
    state = current_games.get(uid, {}).get('math', None)
    if state is None:
        await callback.message.edit_text("Задача не активна. Нажми 'Математический челлендж' чтобы начать.", reply_markup=main_menu())
        return

    if answer == str(state['correct']):
        if child:
            users[child]["points"] += 1
        # удаляем текущее состояние и создаём новую задачу
        current_games[uid].pop('math', None)
        await send_math_task(callback.message, uid)
    else:
        # повторяем ту же задачу
        a, b, op = state['a'], state['b'], state['op']
        options = state['options']
        kb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=str(opt), callback_data=f"math_answer:{opt}:{state['correct']}")] for opt in options
        ] + [[InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]])
        await callback.message.edit_text(f"❌ Неправильно! Подумай ещё раз.\nСколько будет {a} {op} {b}?", reply_markup=kb)

# === ОЧКИ ===
@dp.callback_query(F.data == "points")
async def show_points(callback: CallbackQuery):
    child = get_child(callback.from_user.id)
    await callback.message.edit_text(f"{child}, у тебя {users[child]['points']} очков 🏆", reply_markup=back_menu())

# === КТО Я ===
@dp.callback_query(F.data == "whoami")
async def whoami(callback: CallbackQuery):
    child = get_child(callback.from_user.id)
    data = users[child]
    text = f"👤 Имя: {child}\n🎂 День рождения: {data['birthday']}\n🏆 Очки: {data['points']}"
    await callback.message.edit_text(text, reply_markup=back_menu())

# === СКОЛЬКО ДНЕЙ ДО ДР ===
def days_until(date_str):
    bday = datetime.strptime(date_str, "%Y-%m-%d").date()
    today = datetime.today().date()
    next_bday = bday.replace(year=today.year)
    if next_bday < today:
        next_bday = next_bday.replace(year=today.year + 1)
    return (next_bday - today).days

@dp.callback_query(F.data == "birthday")
async def birthday(callback: CallbackQuery):
    child = get_child(callback.from_user.id)
    days = days_until(users[child]["birthday"])
    await callback.message.edit_text(f"До дня рождения {child} осталось {days} дней 🎉", reply_markup=back_menu())

# === ЗАПУСК БОТА ===
async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
