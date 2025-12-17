from telegram import Update
from telegram.ext import ContextTypes
from telegram.error import NetworkError, TimedOut
from shared.utils.welcome_text import get_welcome_text
from shared.utils.get_welcome_keyboard import get_welcome_keyboard
from repository.analytics import track_start_analytics
import logging

logger = logging.getLogger(__name__)

# Offer expiration period in days
OFFER_EXPIRATION_DAYS = 7


async def start_view(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command - register user, create offer, show welcome"""
    try:
        user = update.effective_user
        user_id = user.id
        nickname = user.username
        first_name = user.first_name
        last_name = user.last_name
        # Ensure is_premium is always a boolean, never None
        is_premium = bool(getattr(user, 'is_premium', False) or False)
        # Collect analytics and persist user/offer
        try:
            track_start_analytics(
                user=user,
                offer_expiration_days=OFFER_EXPIRATION_DAYS
            )
        except Exception as analytics_error:
            logger.error(f"Analytics error in start command: {analytics_error}", exc_info=True)
            # Continue to show welcome even if analytics failed

        # Send welcome message with lesson button
        text = get_welcome_text()
        await update.message.reply_text(text, reply_markup=get_welcome_keyboard(user_id=user_id))

    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error in start command: {e}")
    except Exception as e:
        logger.error(f"Error in start command: {e}", exc_info=True)
        try:
            if update.message:
                await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")
        except (NetworkError, TimedOut):
            pass
        except Exception:
            pass