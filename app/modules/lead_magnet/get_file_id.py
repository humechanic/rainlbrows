"""
Вспомогательный скрипт для получения file_id видео из Telegram

Использование:
1. Временно добавьте этот обработчик в main.py:
   from modules.lead_magnet.get_file_id import get_file_id_handler
   application.add_handler(MessageHandler(filters.VIDEO, get_file_id_handler))

2. Запустите бота
3. Отправьте видео боту в личные сообщения
4. Бот ответит с file_id
5. Скопируйте file_id и вставьте в modules/lead_magnet/config.py
6. Удалите обработчик из main.py
"""
from telegram import Update
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)


async def get_file_id_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Temporary handler to get file_id of uploaded video"""
    if not update.message or not update.message.video:
        return
    
    video = update.message.video
    file_id = video.file_id
    file_unique_id = video.file_unique_id
    file_size = video.file_size
    duration = video.duration
    width = video.width
    height = video.height
    
    text = (
        f"📹 Информация о видео:\n\n"
        f"File ID: `{file_id}`\n"
        f"File Unique ID: `{file_unique_id}`\n"
        f"Размер: {file_size / (1024*1024):.2f} MB\n"
        f"Длительность: {duration} сек\n"
        f"Разрешение: {width}x{height}\n\n"
        f"✅ Скопируйте File ID и вставьте в `modules/lesson/config.py`:\n"
        f"`LESSON_TELEGRAM_VIDEO_FILE_ID = \"{file_id}\"`"
    )
    
    await update.message.reply_text(text, parse_mode='Markdown')
    logger.info(f"Video file_id: {file_id}")

