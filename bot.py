import os
import re
import logging
import requests
from telegram import Update
from telegram.ext import Updater, MessageHandler, Filters, CallbackContext

# Настройка токена
BOT_TOKEN = os.environ.get("BOT_TOKEN") or "7174011610:AAGGjDniBS_D1HE_aGSxPA9M6mrGCZOeqNM"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_oldest_tiktok_video(profile_url: str) -> str:
    """Находит ссылку на самое старое видео TikTok-аккаунта."""
    match = re.search(r"tiktok\\.com/@([A-Za-z0-9._]+)", profile_url)
    if not match:
        raise ValueError("Некорректная ссылка на TikTok-аккаунт.")
    username = match.group(1)

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    url = f"https://www.tiktok.com/@{username}"
    logger.info(f"Fetching TikTok profile for @{username}")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    # Ищем все видео
    video_ids = re.findall(r'/video/(\\d+)', response.text)
    if not video_ids:
        raise RuntimeError("Не удалось найти видео у этого пользователя.")

    # Убираем дубликаты и берём последнее (старейшее)
    video_ids = list(dict.fromkeys(video_ids))
    oldest_id = video_ids[-1]
    return f"https://www.tiktok.com/@{username}/video/{oldest_id}"

def start_message(update: Update, context: CallbackContext):
    """Отправляет приветственное сообщение при старте."""
    update.message.reply_text(
        "👋 Привет! Пришли мне ссылку на TikTok-аккаунт, например:\n"
        "https://www.tiktok.com/@username\n\n"
        "Я пришлю ссылку на самое старое видео этого аккаунта 🔗"
    )

def handle_tiktok_link(update: Update, context: CallbackContext):
    """Обрабатывает ссылку TikTok и отвечает ссылкой на старое видео."""
    text = update.message.text.strip()
    if "tiktok.com" not in text:
        update.message.reply_text("❌ Это не похоже на ссылку TikTok. Попробуй ещё раз 🙂")
        return

    try:
        video_url = get_oldest_tiktok_video(text)
        update.message.reply_text(f"📹 Самое старое видео этого аккаунта:\n{video_url}")
    except Exception as e:
        logger.exception(e)
        update.message.reply_text(f"⚠️ Ошибка: {e}")

def main():
    updater = Updater(BOT_TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(MessageHandler(Filters.command, start_message))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_tiktok_link))

    logger.info("Bot started.")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
