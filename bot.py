import os
import re
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN") or "7174011610:AAGGjDniBS_D1HE_aGSxPA9M6mrGCZOeqNM"

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_oldest_tiktok_video(profile_url: str) -> str:
    """Находит ссылку на самое старое видео TikTok-аккаунта."""
    match = re.search(r"tiktok\\.com/@([A-Za-z0-9._]+)", profile_url)
    if not match:
        raise ValueError("Некорректная ссылка на TikTok-аккаунт.")
    username = match.group(1)

    headers = {"User-Agent": "Mozilla/5.0"}
    url = f"https://www.tiktok.com/@{username}"
    logger.info(f"Fetching TikTok profile for @{username}")
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()

    video_ids = re.findall(r'/video/(\\d+)', response.text)
    if not video_ids:
        raise RuntimeError("Не удалось найти видео у этого пользователя.")

    # Убираем дубликаты и берём последнее (старейшее)
    video_ids = list(dict.fromkeys(video_ids))
    oldest_id = video_ids[-1]
    return f"https://www.tiktok.com/@{username}/video/{oldest_id}"

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обрабатывает любое сообщение."""
    text = update.message.text.strip()

    if "tiktok.com" not in text:
        await update.message.reply_text(
            "👋 Привет! Пришли ссылку на TikTok-аккаунт, например:\n"
            "https://www.tiktok.com/@username\n\n"
            "Я пришлю ссылку на самое старое видео этого аккаунта 🔗"
        )
        return

    try:
        video_url = get_oldest_tiktok_video(text)
        await update.message.reply_text(f"📹 Самое старое видео:\n{video_url}")
    except Exception as e:
        logger.exception(e)
        await update.message.reply_text(f"⚠️ Ошибка: {e}")

async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    logger.info("Bot started.")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
