from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from shared.utils.get_back import get_back_keyboard
from modules.lead_magnet.config import get_lead_magnet_config
from db.session import get_db_session
from db.repository import get_or_create_user, mark_lesson_clicked
from scheduler.job_queue_reminders import schedule_lead_reminders
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
    
    # Try to use database-based reminder system first
    # If database is unavailable, fallback to JobQueue-based system
    db_available = False
    try:
        db = get_db_session()
        try:
            # Test database connection by trying to get or create user
            db_user = get_or_create_user(
                db=db,
                telegram_id=user_id,
                nickname=update.effective_user.username,
                first_name=update.effective_user.first_name,
                last_name=update.effective_user.last_name,
                is_premium=bool(getattr(update.effective_user, 'is_premium', False) or False)
            )
            
            # Mark lesson clicked - this triggers database-based reminder system
            # (process_reminders in scheduler/reminders.py will pick it up)
            offer = mark_lesson_clicked(db, db_user.id)
            
            if offer:
                db_available = True
                logger.info(f"Database available: marked lesson clicked for user_id={user_id}, offer_id={offer.id}. Using database-based reminder system.")
            else:
                logger.warning(f"Database available but no offer found for user_id={user_id}. Will use JobQueue fallback.")
        except Exception as db_error:
            logger.warning(f"Database error in handle_get_lead_magnet: {db_error}. Will use JobQueue fallback.")
            db_available = False
        finally:
            db.close()
    except Exception as db_session_error:
        logger.warning(f"Could not get database session: {db_session_error}. Will use JobQueue fallback.")
        db_available = False
    
    # Fallback to JobQueue-based reminder system if database is not available
    if not db_available:
        try:
            # Check if JobQueue is available before trying to use it
            try:
                job_queue = context.job_queue
                if job_queue is None:
                    raise AttributeError("JobQueue is None")
            except AttributeError:
                logger.warning("JobQueue is not available. Reminders will not be sent. Install python-telegram-bot[job-queue] to enable fallback reminder system.")
                # Continue - user still gets the lesson even if reminders can't be scheduled
                return
            
            # Use minutes for testing, set to False for production (uses hours)
            use_minutes = false  # Set to False in production
            schedule_lead_reminders(context, user_id, use_minutes=use_minutes)
            logger.info(f"Database unavailable: scheduled lead reminders for user_id={user_id} using JobQueue (fallback mode)")
        except Exception as reminder_error:
            logger.error(f"Error scheduling reminders via JobQueue for user_id={user_id}: {reminder_error}", exc_info=True)
            # Continue even if reminder scheduling fails - user still gets the lesson
    
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

