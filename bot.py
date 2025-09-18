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

# === ВИКТОРИНА (пример — вставь свой полный список вопросов тут) ===
quiz_questions = [
    ("Столица Франции?", ["Париж", "Лондон", "Берлин", "Рим"], "Париж"),
    ("Самая длинная река в мире?", ["Амазонка", "Нил", "Волга", "Янцзы"], "Нил"),
    ("Как называется спутник Земли?", ["Марс", "Луна", "Венера", "Сатурн"], "Луна"),
]

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

# === ВИКТОРИНА ===
@dp.callback_query(F.data == "quiz_start")
async def start_quiz(callback: CallbackQuery):
    user_name = get_child(callback.from_user.id)
    if not user_name:
        await callback.message.edit_text("Играть могут только зарегистрированные дети.", reply_markup=back_menu())
        return

    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать", callback_data="quiz_begin")],
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back")]
        ]
    )
    try:
        await callback.message.edit_text(
            f"🧠 Викторина!\n\nПравила:\n✅ Правильный ответ: +1 очко\n❌ Неправильный ответ: -1 очко\nУдачи, {user_name}!",
            reply_markup=kb
        )
    except TelegramBadRequest:
        pass

@dp.callback_query(F.data == "quiz_begin")
async def begin_quiz(callback: CallbackQuery):
    user_id = callback.from_user.id
    questions = quiz_questions.copy()
    random.shuffle(questions)
    active_quiz[user_id] = {"question_index": 0, "questions": questions, "last_text": callback.message}
    await send_quiz_question(user_id, callback.message.chat.id)

async def send_quiz_question(user_id, chat_id, result_text=""):
    quiz = active_quiz.get(user_id)
    if not quiz:
        return

    q_index = quiz["question_index"]

    if q_index >= len(quiz["questions"]):
        user_name = get_child(user_id)
        final_text = f"Викторина закончена! Твои очки: {users[user_name]['points']}"
        try:
            await quiz["last_text"].edit_text(final_text, reply_markup=back_menu())
        except TelegramBadRequest:
            pass
        del active_quiz[user_id]
        return

    question, options, _ = quiz["questions"][q_index]

    kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"quiz_ans:{i}")] for i, opt in enumerate(options)]
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

@dp.callback_query(F.data.startswith("quiz_ans:"))
async def quiz_answer(callback: CallbackQuery):
    await callback.answer()

    user_id = callback.from_user.id
    if user_id not in active_quiz:
        await callback.message.answer("Викторина не активна")
        return

    quiz = active_quiz[user_id]
    q_index = quiz["question_index"]
    question, options, correct_answer = quiz["questions"][q_index]
    chosen_index = int(callback.data.split(":")[1])
    chosen_answer = options[chosen_index]

    user_name = get_child(user_id)

    if chosen_answer == correct_answer:
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
