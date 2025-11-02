import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# ==================== Таблица шифра ====================
cipher_table = {
    'А': '☀', 'Б': '☁', 'В': '♣', 'Г': '♦', 'Д': '♥', 'Е': '░', 'Ж': '▒',
    'З': '▓', 'И': '♤', 'Й': '♧', 'К': '♨', 'Л': '☯', 'М': '☘', 'Н': '☂',
    'О': '☽', 'П': '♠', 'Р': '☢', 'С': '☣', 'Т': '☡', 'У': '☮', 'Ф': '☾',
    'Х': '☹', 'Ц': '♢', 'Ч': 'd', 'Ш': '✧', 'Щ': '★', 'Ы': '☆', 'Ь': '✩',
    'Э': '✪', 'Ю': '✫', 'Я': '✬', 'Ё': 'q',
    'а': '❀', 'б': '❁', 'в': '❂', 'г': '❃', 'д': '❄', 'е': '❅', 'ж': '❆',
    'з': '❇', 'и': '❈', 'й': '❉', 'к': '❊', 'л': '❋', 'м': '●', 'н': '○',
    'о': '◐', 'п': '◑', 'р': '◒', 'с': '◓', 'т': '◔', 'у': '◕', 'ф': '◖',
    'х': '◗', 'ц': '◘', 'ч': '◙', 'ш': '◚', 'щ': '◛', 'ы': '◜', 'ь': '◝',
    'э': '◞', 'ю': '◟', 'я': '◠', 'ё': 'b',
    '0': '⊙', '1': '⊕', '2': '⊗', '3': '⊘', '4': '⊛', '5': '⊝', '6': '⊞', '7': '⊟', '8': '⊠', '9': '⊡',
    ' ': '•', ',': '✕', '.': '✦', '!': '⚡', '?': '☄', '-': '–', ':': '∶', ';': '⁏', '(': '❨', ')': '❩'
}

decipher_table = {v: k for k, v in cipher_table.items()}
KEY_SYMBOL = '🔑'  # Ключевой символ для распознавания шифра

# ==================== Функции ====================
def encrypt(text):
    return ''.join(cipher_table.get(ch, ch) for ch in text) + KEY_SYMBOL

def decrypt(text):
    if text.endswith(KEY_SYMBOL):
        text = text[:-1]
    return ''.join(decipher_table.get(ch, ch) for ch in text)

def is_encrypted(text):
    return text.endswith(KEY_SYMBOL)

# ==================== Настройки ====================
CHANNEL_ID = "@salwasser_bot_live"
BOT_LINK = "@salwasser_bot"

# ==================== Обработчики ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришлите текст, который хотите зашифровать или расшифровать.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    username = update.message.from_user.username or update.message.from_user.first_name

    if is_encrypted(user_text):
        result = decrypt(user_text)
        text_for_channel = result
    else:
        result = encrypt(user_text)
        text_for_channel = user_text

    # Ответ пользователю
    await update.message.reply_text(result)

    # Попытка отправить в канал (если бот не админ — просто пропускаем)
    channel_message = f"@{username}\n\"{text_for_channel}\"\n\n{BOT_LINK}"
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=channel_message)
    except Exception as e:
        print(f"⚠️ Ошибка отправки в канал: {e}")

# ==================== Запуск бота ====================
if __name__ == "__main__":
    TOKEN = os.getenv("BOT_TOKEN")  # Берём токен из переменных окружения
    if not TOKEN:
        raise ValueError("❌ Переменная окружения BOT_TOKEN не установлена!")

    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("✅ Бот запущен...")
    app.run_polling()
