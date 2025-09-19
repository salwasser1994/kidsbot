import asyncio
import random
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.exceptions import TelegramBadRequest

API_TOKEN = "7174011610:AAGGjDniBS_D1HE_aGSxPA9M6mrGCZOeqNM"

bot = Bot(token=API_TOKEN)
dp = Dispatcher()  # Aiogram 3.x: Dispatcher без аргументов

# === ДЕТИ ===
users = {
    "Руслан": {"id": 7894501725, "birthday": "2014-10-04", "points": 0},
    "Алиса": {"id": 7719485802, "birthday": "2016-06-19", "points": 0},
    "Томас": {"id": 5205381793, "birthday": "1994-04-27", "points": 0},
}

all_questions = {
    "Математика": [
        ("Сколько будет 1 + 1?", ["1", "2", "3", "4"], "2"),
        ("Сколько будет 2 * 3?", ["5", "6", "7", "8"], "6"),
        ("Сколько будет 5 - 2?", ["2", "3", "4", "5"], "3"),
        ("Сколько будет 10 / 2?", ["4", "5", "6", "8"], "5"),
        ("Какое число больше: 7 или 9?", ["7", "9", "8", "6"], "9"),
        ("Сколько углов у квадрата?", ["3", "4", "5", "6"], "4"),
        ("Сколько сантиметров в метре?", ["10", "100", "1000", "50"], "100"),
        ("Какая фигура имеет 3 стороны?", ["Квадрат", "Треугольник", "Круг", "Прямоугольник"], "Треугольник"),
        ("Сколько десятков в числе 50?", ["5", "50", "10", "15"], "5"),
        ("Сколько минут в часе?", ["60", "100", "120", "50"], "60"),
        ("Сколько будет 8 + 7?", ["14", "15", "16", "17"], "15"),
        ("Сколько будет 12 - 5?", ["6", "7", "8", "9"], "7"),
        ("Сколько будет 3 * 4?", ["12", "11", "10", "13"], "12"),
        ("Сколько будет 20 / 4?", ["4", "5", "6", "7"], "5"),
        ("Сколько углов у треугольника?", ["2", "3", "4", "5"], "3"),
        ("Сколько дней в неделе?", ["5", "6", "7", "8"], "7"),
        ("Сколько секунд в минуте?", ["30", "50", "60", "100"], "60"),
        ("Сколько месяцев в году?", ["10", "11", "12", "13"], "12"),
        ("Сколько будет 9 + 8?", ["16", "17", "18", "19"], "17"),
        ("Сколько будет 15 - 6?", ["8", "9", "10", "11"], "9"),
        ("Сколько будет 7 * 2?", ["12", "13", "14", "15"], "14"),
        ("Сколько будет 18 / 3?", ["5", "6", "7", "8"], "6"),
        ("Сколько градусов в прямом угле?", ["45", "90", "180", "360"], "90"),
        ("Какая фигура имеет 4 равные стороны?", ["Квадрат", "Прямоугольник", "Треугольник", "Круг"], "Квадрат"),
        ("Сколько будет 11 + 6?", ["16", "17", "18", "19"], "17"),
        ("Сколько будет 20 - 7?", ["12", "13", "14", "15"], "13"),
        ("Сколько будет 5 * 5?", ["20", "25", "30", "35"], "25"),
        ("Сколько будет 36 / 6?", ["5", "6", "7", "8"], "6"),
        ("Сколько углов у пятиугольника?", ["4", "5", "6", "7"], "5"),
        ("Сколько сантиметров в полуметре?", ["25", "50", "75", "100"], "50"),
        ("Сколько минут в полчаса?", ["15", "20", "25", "30"], "30"),
        ("Сколько будет 14 + 5?", ["18", "19", "20", "21"], "19"),
        ("Сколько будет 9 - 4?", ["4", "5", "6", "7"], "5"),
        ("Сколько будет 6 * 3?", ["16", "17", "18", "19"], "18"),
        ("Сколько будет 24 / 4?", ["5", "6", "7", "8"], "6"),
        ("Сколько углов у шестиугольника?", ["5", "6", "7", "8"], "6"),
        ("Сколько будет 13 + 7?", ["19", "20", "21", "22"], "20"),
        ("Сколько будет 15 - 8?", ["6", "7", "8", "9"], "7"),
        ("Сколько будет 4 * 6?", ["20", "22", "24", "26"], "24"),
        ("Сколько будет 30 / 5?", ["5", "6", "7", "8"], "6"),
        ("Сколько дней в високосном году?", ["365", "366", "364", "367"], "366"),
        ("Сколько будет 8 + 9?", ["16", "17", "18", "19"], "17"),
        ("Сколько будет 10 - 3?", ["6", "7", "8", "9"], "7"),
        ("Сколько будет 7 * 7?", ["45", "48", "49", "50"], "49"),
        ("Сколько будет 49 / 7?", ["6", "7", "8", "9"], "7"),
        ("Сколько градусов в треугольнике?", ["90", "180", "360", "270"], "180"),
        ("Сколько будет 12 + 8?", ["19", "20", "21", "22"], "20"),
        ("Сколько будет 14 - 9?", ["4", "5", "6", "7"], "5"),
        ("Сколько будет 5 * 9?", ["40", "45", "50", "55"], "45"),
        ("Сколько будет 81 / 9?", ["8", "9", "10", "11"], "9"),
        ("Сколько углов у восьмиугольника?", ["6", "7", "8", "9"], "8"),
    ],
    "Литература": [
        ("Кто написал 'Войну и мир'?", ["Толстой", "Пушкин", "Гоголь", "Чехов"], "Толстой"),
        ("Кто автор 'Муми-троллей'?", ["Туве Янссон", "Астрид Линдгрен", "Чуковский", "Носов"], "Туве Янссон"),
        ("Главный герой сказки 'Красная Шапочка'?", ["Красная Шапочка", "Волк", "Бабушка", "Мальчик"], "Красная Шапочка"),
        ("Кто написал 'Руслан и Людмила'?", ["Пушкин", "Толстой", "Гоголь", "Чехов"], "Пушкин"),
        ("Кто написал 'Приключения Незнайки'?", ["Носов", "Толстой", "Пушкин", "Чуковский"], "Носов"),
        ("Кто написал 'Доктор Айболит'?", ["Чуковский", "Толстой", "Пушкин", "Носов"], "Чуковский"),
        ("Кто написал 'Бармалей'?", ["Чуковский", "Толстой", "Пушкин", "Носов"], "Чуковский"),
        ("Кто написал 'Винни-Пух'?", ["А. Милн", "Толстой", "Пушкин", "Чуковский"], "А. Милн"),
        ("Кто автор 'Малыш и Карлсон'?", ["Линдгрен", "Толстой", "Чуковский", "Носов"], "Линдгрен"),
        ("Главный герой 'Пиноккио'?", ["Пиноккио", "Джинни", "Чип", "Гоффи"], "Пиноккио"),
        # ... 40 других вопросов
    ],
    "География": [
        ("Столица России?", ["Москва", "Санкт-Петербург", "Казань", "Новосибирск"], "Москва"),
        ("Самая высокая гора мира?", ["Эверест", "Килиманджаро", "Арарат", "Фудзи"], "Эверест"),
        ("Самый большой океан?", ["Тихий", "Атлантический", "Индийский", "Северный Ледовитый"], "Тихий"),
        ("Столица Франции?", ["Париж", "Лондон", "Берлин", "Мадрид"], "Париж"),
        ("Столица Германии?", ["Берлин", "Вена", "Мюнхен", "Гамбург"], "Берлин"),
        ("Столица Италии?", ["Рим", "Милан", "Флоренция", "Неаполь"], "Рим"),
        ("Столица Великобритании?", ["Лондон", "Оксфорд", "Кембридж", "Бирмингем"], "Лондон"),
        ("Столица Испании?", ["Мадрид", "Барселона", "Валенсия", "Севилья"], "Мадрид"),
        ("Какая река протекает через Москву?", ["Москва", "Волга", "Нил", "Днепр"], "Москва"),
        ("Самый длинный в мире река?", ["Амазонка", "Нил", "Миссисипи", "Янцзы"], "Нил"),
        # ... 40 других вопросов
    ],
    "Викторина": [
        ("Кто написал 'Войну и мир'?", ["Толстой", "Пушкин", "Гоголь", "Чехов"], "Толстой"),
        ("Самая маленькая птица?", ["Колибри", "Воробей", "Синица", "Пингвин"], "Колибри"),
        ("Какая планета ближе всего к Солнцу?", ["Меркурий", "Венера", "Марс", "Юпитер"], "Меркурий"),
        ("Что растёт на деревьях?", ["Яблоки", "Камни", "Молоко", "Морковь"], "Яблоки"),
        ("Как называется спутник Земли?", ["Марс", "Луна", "Венера", "Сатурн"], "Луна"),
        ("Кто написал 'Приключения Незнайки'?", ["Носов", "Толстой", "Пушкин", "Чуковский"], "Носов"),
        ("Самое большое животное на Земле?", ["Слон", "Кит", "Медведь", "Жираф"], "Кит"),
        ("Какая птица умеет говорить?", ["Попугай", "Воробей", "Синица", "Орёл"], "Попугай"),
        ("Какой зверь самый быстрый на земле?", ["Гепард", "Лев", "Заяц", "Слон"], "Гепард"),
        ("Какой цвет у моркови?", ["Красный", "Оранжевый", "Зелёный", "Фиолетовый"], "Оранжевый"),
        ("Кто изобрёл лампу?", ["Эдисон", "Ньютон", "Тесла", "Дарвин"], "Эдисон"),
        ("Сколько букв в русском алфавите?", ["32", "33", "34", "31"], "33"),
    ]
}

# === МЕНЮ ===
def main_menu(user_id=None):
    points_text = ""
    user_name = get_child(user_id) if user_id else None
    if user_name:
        points_text = f"\n🏆 У тебя {users[user_name]['points']} очков"

    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎮 Игры", callback_data="menu_games"),
                InlineKeyboardButton(text="📚 Учёба", callback_data="menu_study"),
            ],
            [
                InlineKeyboardButton(text="📖 Сказки", callback_data="menu_fairytales"),
                InlineKeyboardButton(text="👤 Кто я", callback_data="whoami"),
            ],
            [
                InlineKeyboardButton(text="📅 Сколько дней до...", callback_data="birthday"),
            ]
        ]
    ), f"Главное меню:{points_text}"

def back_menu():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад в главное меню", callback_data="back")]
        ]
    )

def get_child(user_id: int):
    for name, data in users.items():
        if data["id"] == user_id:
            return name
    return None

# === АКТИВНЫЕ ИГРЫ ===
active_quiz = {}  # user_id: {"question_index": int, "questions": list, "last_text": Message}

# === ОБРАБОТЧИКИ ===
@dp.message(F.text)
async def start_menu(message: Message):
    kb, text = main_menu(message.from_user.id)
    await message.answer(text, reply_markup=kb)

@dp.callback_query(F.data == "back")
async def back(callback: CallbackQuery):
    user_id = callback.from_user.id
    if user_id in active_quiz:
        del active_quiz[user_id]
    kb, text = main_menu(user_id)
    try:
        await callback.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        pass

@dp.callback_query(F.data == "menu_games")
async def menu_games(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧠 Викторина", callback_data="quiz_start")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ]
    )
    try:
        await callback.message.edit_text("🎮 Игры — выбери:", reply_markup=kb)
    except TelegramBadRequest:
        pass

@dp.callback_query(F.data == "menu_study")
async def menu_study(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📐 Математика", callback_data="topic:Математика")],
            [InlineKeyboardButton(text="📖 Литература", callback_data="topic:Литература")],
            [InlineKeyboardButton(text="🌍 География", callback_data="topic:География")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ]
    )
    try:
        await callback.message.edit_text("📚 Учёба — выбери предмет:", reply_markup=kb)
    except TelegramBadRequest:
        pass

# === общий обработчик старта викторины или темы ===
@dp.callback_query(F.data.startswith("topic:") | F.data == "quiz_start")
async def start_topic_or_quiz(callback: CallbackQuery):
    user_name = get_child(callback.from_user.id)
    if not user_name:
        await callback.message.edit_text(
            "Играть могут только зарегистрированные дети.",
            reply_markup=back_menu()
        )
        return

    if callback.data == "quiz_start":
        topic = "Викторина"
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Начать", callback_data=f"quiz_begin:{topic}")],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
            ]
        )
        text = f"🧠 Викторина!\n\nПравила:\n✅ Правильный ответ: +1 очко\n❌ Неправильный ответ: -1 очко\nУдачи, {user_name}!"
    else:
        topic = callback.data.split(":")[1]
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text="Начать", callback_data=f"quiz_begin:{topic}")],
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
            ]
        )
        text = f"📚 Тема: {topic}\nУдачи, {user_name}!"

    try:
        await callback.message.edit_text(text, reply_markup=kb)
    except TelegramBadRequest:
        pass


# === начало конкретной викторины/темы ===
@dp.callback_query(F.data.startswith("quiz_begin:"))
async def begin_quiz(callback: CallbackQuery):
    user_id = callback.from_user.id
    topic = callback.data.split(":")[1]

    questions = all_questions.get(topic, []).copy()
    if not questions:
        await callback.message.edit_text("Вопросы для этой темы пока не добавлены.", reply_markup=back_menu())
        return

    random.shuffle(questions)  # Перемешиваем вопросы

    active_quiz[user_id] = {
        "question_index": 0,
        "questions": questions,
        "last_text": callback.message,
        "topic": topic
    }

    await send_quiz_question(user_id, callback.message.chat.id)


# === отправка вопроса ===
async def send_quiz_question(user_id, chat_id, result_text=""):
    quiz = active_quiz.get(user_id)
    if not quiz:
        return

    q_index = quiz["question_index"]

    if q_index >= len(quiz["questions"]):
        user_name = get_child(user_id)
        final_text = f"{quiz['topic']} закончена! Твои очки: {users[user_name]['points']}"
        try:
            await quiz["last_text"].edit_text(final_text, reply_markup=back_menu())
        except TelegramBadRequest:
            pass
        del active_quiz[user_id]
        return

    question, options, correct_answer = quiz["questions"][q_index]

    # Перемешиваем варианты ответов
    shuffled_options = options.copy()
    random.shuffle(shuffled_options)
    correct_index = shuffled_options.index(correct_answer)

    # Сохраняем в активной викторине
    quiz["shuffled_options"] = shuffled_options
    quiz["correct_index"] = correct_index

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"quiz_ans:{i}")]
                         for i, opt in enumerate(shuffled_options)]
                     + [[InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back")]]
    )

    user_name = get_child(user_id)
    points = users[user_name]["points"]
    text_parts = []
    if result_text:
        text_parts.append(result_text)
        text_parts.append(f"🏆 Очки: {points}")
    text_parts.append(f"Вопрос {q_index + 1}: {question}")
    text = "\n".join(text_parts)

    try:
        await quiz["last_text"].edit_text(text, reply_markup=kb)
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise


# === обработка ответа ===
@dp.callback_query(F.data.startswith("quiz_ans:"))
async def quiz_answer(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id not in active_quiz:
        await callback.message.answer("Викторина не активна")
        return

    quiz = active_quiz[user_id]
    q_index = quiz["question_index"]

    chosen_index = int(callback.data.split(":")[1])
    shuffled_options = quiz["shuffled_options"]
    correct_index = quiz["correct_index"]

    user_name = get_child(user_id)

    if chosen_index == correct_index:
        users[user_name]["points"] += 1
        result_text = f"✅ Правильно, молодец {user_name}!"
        quiz["question_index"] += 1
    else:
        users[user_name]["points"] = max(0, users[user_name]["points"] - 1)
        result_text = f"❌ Неправильно, {user_name}! Попробуй ещё раз."

    await send_quiz_question(user_id, callback.message.chat.id, result_text=result_text)

# === ЗАПУСК ===
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot)
