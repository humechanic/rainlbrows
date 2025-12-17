from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from shared.utils.get_back import get_back_keyboard
from modules.lead_magnet.config import get_lead_magnet_config
from db.session import get_db_session
from db.repository import get_or_create_user, mark_lesson_clicked
import os
import logging

logger = logging.getLogger(__name__)


async def handle_get_lead_magnet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle 'Забрать урок' callback - send lesson video and mark click time"""
    query = update.callback_query
    await query.answer()
    
    user_id = update.effective_user.id
    bot = context.bot
    config = get_lead_magnet_config()
    
    # Mark lesson clicked in database for reminder scheduling
    db = get_db_session()
    try:
        # Get or create user
        db_user = get_or_create_user(
            db=db,
            telegram_id=user_id,
            nickname=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
            is_premium=bool(getattr(update.effective_user, 'is_premium', False) or False)
        )
        
        # Mark lesson clicked - reminders will be sent automatically by periodic task
        offer = mark_lesson_clicked(db, db_user.id)
        
        if offer:
            logger.info(f"Marked lesson clicked for user_id={user_id}, offer_id={offer.id}. Reminders will be sent automatically by periodic task.")
        else:
            logger.warning(f"No offer found for user_id={user_id}, cannot mark lesson clicked")
    except Exception as db_error:
        logger.error(f"Database error in handle_get_lead_magnet: {db_error}", exc_info=True)
    finally:
        db.close()
    
    # Get lesson description
    description = config["description"]
    
    try:
        # Option 1: YouTube link (simplest)
        if config["youtube_url"] and config["youtube_url"] != "https://www.youtube.com/watch?v=YOUR_VIDEO_ID":
            text = f"{description}\n\n📺 Смотри урок на YouTube:\n{config['youtube_url']}"
            await query.message.reply_text(text, reply_markup=get_back_keyboard())
            return
        
        # Option 2: Telegram video by file_id (if video already uploaded to Telegram)
        if config["telegram_file_id"]:
            try:
                await bot.send_video(
                    chat_id=user_id,
                    video=config["telegram_file_id"],
                    caption=description
                )
                await bot.send_message(
                    chat_id=user_id,
                    text="✅ Урок отправлен!",
                    reply_markup=get_back_keyboard()
                )
                return
            except TelegramError as e:
                logger.error(f"Error sending video by file_id: {e}")
                # Fallback to file upload if file_id doesn't work
        
        # Option 3: Local video file (upload from disk)
        if config["video_file_path"] and os.path.exists(config["video_file_path"]):
            try:
                with open(config["video_file_path"], "rb") as video_file:
                    await bot.send_video(
                        chat_id=user_id,
                        video=video_file,
                        caption=description
                    )
                await bot.send_message(
                    chat_id=user_id,
                    text="✅ Урок отправлен!",
                    reply_markup=get_back_keyboard()
                )
                return
            except FileNotFoundError:
                logger.error(f"Video file not found: {config['video_file_path']}")
            except Exception as e:
                logger.error(f"Error sending video file: {e}")
        
        # Fallback: no video configured
        text = (
            f"{description}\n\n"
            "⚠️ Видео урок временно недоступен.\n"
            "Пожалуйста, настройте конфигурацию урока в modules/lead_magnet/config.py"
        )
        await query.message.reply_text(text, reply_markup=get_back_keyboard())
        
    except Exception as e:
        logger.error(f"Error in handle_get_lesson: {e}", exc_info=True)
        text = "❌ Произошла ошибка при отправке урока. Пожалуйста, попробуйте позже."
        await query.message.reply_text(text, reply_markup=get_back_keyboard())

