import logging
import env

# Import database session lazily to avoid initialization errors
# This allows the app to start even if database is not available
try:
    from db.session import get_db_session
    DB_AVAILABLE = True
except Exception as e:
    logging.warning(f"Database session not available: {e}. Some features will be disabled.")
    DB_AVAILABLE = False
    get_db_session = None

from telegram import Update
from telegram.error import NetworkError, TimedOut, RetryAfter
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# Import scheduler only if database is available
if DB_AVAILABLE:
    try:
from scheduler.reminders import process_reminders
        REMINDERS_AVAILABLE = True
    except Exception as e:
        logging.warning(f"Database-based reminders not available: {e}. Will use JobQueue fallback only.")
        REMINDERS_AVAILABLE = False
        process_reminders = None
else:
    REMINDERS_AVAILABLE = False
    process_reminders = None
from modules.init.start import start_view
from shared.routers.callback_router import route_callback
from shared.constants.callback_register import COMMAND_START
from modules.payment.index import (
    pre_checkout_handler,
    successful_payment_handler,
    failed_payment_handler,
    get_promocode_conversation_handler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log errors and prevent bot crashes"""
    logger = logging.getLogger(__name__)
    error = context.error
    
    # Handle network errors specifically
    if isinstance(error, NetworkError):
        logger.warning(f"Network error occurred: {error}. This is usually temporary.")
        # Don't try to send message on network error - it will likely fail too
        return
    
    if isinstance(error, TimedOut):
        logger.warning(f"Request timed out: {error}. This is usually temporary.")
        return
    
    if isinstance(error, RetryAfter):
        logger.warning(f"Rate limit exceeded. Need to wait {error.retry_after} seconds.")
        return
    
    # Log other errors
    logger.error(f"Exception while handling an update: {error}", exc_info=error)
    
    # Try to notify user about error (only if it's not a network error)
    if update and isinstance(update, Update):
        try:
            if update.message:
                await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")
            elif update.callback_query:
                await update.callback_query.answer("Произошла ошибка. Пожалуйста, попробуйте позже.", show_alert=True)
        except (NetworkError, TimedOut):
            # Don't log network errors when trying to send error message
            pass
        except Exception:
            pass

def setup_handlers(application):
    """Register all handlers for the bot"""
    # Command handlers
    application.add_handler(CommandHandler(COMMAND_START, start_view))
    
    # Promocode conversation handler (must be before CallbackQueryHandler)
    application.add_handler(get_promocode_conversation_handler())
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(route_callback))
    
    # Payment handlers
    application.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))
    
    # Error handler (must be last)
    application.add_error_handler(error_handler)


def setup_jobs(application):
    """Setup scheduled jobs for reminders"""
    job_queue = application.job_queue
    
    if job_queue is None:
        logging.warning("JobQueue is not available. Reminders will not work.")
        return
    
    # Schedule database-based reminder processing if available
    if REMINDERS_AVAILABLE and process_reminders is not None:
    # Schedule reminder processing every 1 minute (for testing)
    # This will check database and send reminders to users who need them
    job_queue.run_repeating(
        callback=process_reminders,
        interval=60,  # 1 minute in seconds (for testing)
        first=10,  # Start after 10 seconds
        name='process_reminders'
    )
        logging.info("Scheduled database-based reminder processing: every 1 minute (testing mode)")
    else:
        logging.info("Database-based reminders not available. Using JobQueue fallback only.")


def main():
    """Initialize and run the bot"""
    logger = logging.getLogger(__name__)
    
    # Initialize database
    try:
        from db.init_db import init_db
        init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize database: {e}", exc_info=True)
        # Continue anyway - database might already exist
    
    # Configure timeouts to handle network issues better
    application = (
        ApplicationBuilder()
        .token(env.TELEGRAM_TOKEN)
        .read_timeout(30)  # Read timeout for requests
        .write_timeout(30)  # Write timeout for requests
        .connect_timeout(30)  # Connection timeout
        .pool_timeout(30)  # Pool timeout
        .get_updates_read_timeout(30)  # Timeout for getUpdates
        .build()
    )
    
    setup_handlers(application)
    setup_jobs(application)
    
    application.run_polling()


if __name__ == '__main__':
    main()
