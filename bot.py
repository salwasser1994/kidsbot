from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, CommandHandler, filters

# ==================== Таблица шифра ====================
cipher_table = {
    # Заглавные буквы
    'А': '☀', 'Б': '☁', 'В': '♣', 'Г': '♦', 'Д': '♥', 'Е': '░', 'Ж': '▒',
    'З': '▓', 'И': '♤', 'Й': '♧', 'К': '♨', 'Л': '☯', 'М': '♠', 'Н': '☢',
    'О': '☽', 'П': '♠', 'Р': '☯', 'С': '☢', 'Т': '♦', 'У': '☮', 'Ф': '☾',
    'Х': '☹', 'Ц': '♣', 'Ч': '☀', 'Ш': '☂', 'Щ': '☁', 'Ы': '♤', 'Ь': '☯',
    'Э': '░', 'Ю': '☼', 'Я': '☀',
    # Маленькие буквы (уникальные символы)
    'а': '⚡', 'б': '❄', 'в': '☃', 'г': '☾', 'д': '☼', 'е': '☽', 'ж': '♨',
    'з': '♧', 'и': '♤', 'й': '♣', 'к': '♦', 'л': '♥', 'м': '♢', 'н': '♣',
    'о': '♠', 'п': '☯', 'р': '☂', 'с': '☁', 'т': '⚡', 'у': '❆', 'ф': '❅',
    'х': '✦', 'ц': '✧', 'ч': '❉', 'ш': '❋', 'щ': '❖', 'ы': '✪', 'ь': '✫',
    'э': '✬', 'ю': '✭', 'я': '✮',
    # Цифры
    '0':'①', '1':'②', '2':'③', '3':'④', '4':'⑤', '5':'⑥', '6':'⑦', '7':'⑧', '8':'⑨', '9':'⑩',
    # Знаки препинания
    ' ': '•', ',': '✕', '.': '✦', '!': '⚡', '?': '☄', '-': '–', ':': '∶', ';': '⁏', '(': '❨', ')': '❩'
}

decipher_table = {v: k for k, v in cipher_table.items()}

# ==================== Функции ====================
def encrypt(text):
    return ''.join(cipher_table.get(ch, ch) for ch in text)

def decrypt(text):
    return ''.join(decipher_table.get(ch, ch) for ch in text)

def is_encrypted(text):
    return any(ch in decipher_table for ch in text)

# ==================== Настройки ====================
CHANNEL_ID = "@your_channel_username"  # замените на username вашего канала
BOT_LINK = "https://t.me/YourBotUsername"  # ссылка на бота для рекламы

# ==================== Обработчики ====================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Пришлите текст который хотите обработать")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    username = update.message.from_user.username or update.message.from_user.first_name

    # Определяем действие
    if is_encrypted(user_text):
        result = decrypt(user_text)
        text_for_channel = result
    else:
        result = encrypt(user_text)
        text_for_channel = user_text

    # Ответ пользователю
    await update.message.reply_text(result)

    # Отправка в канал
    channel_message = f"{username}\n\"{text_for_channel}\"\n\nПосмотрите бота: {BOT_LINK}"
    await context.bot.send_message(chat_id=CHANNEL_ID, text=channel_message)

# ==================== Запуск бота ====================
if __name__ == "__main__":
    TOKEN = "7174011610:AAGGjDniBS_D1HE_aGSxPA9M6mrGCZOeqNM"  # вставьте токен вашего бота
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Бот запущен...")
    app.run_polling()
