"""
Reminder processor module.

This module contains the main function that processes all reminders
by checking the database and sending messages to users.
"""
from db.session import get_db_session
from db.repository import (
    get_users_for_last_call_reminder,
    get_users_for_regular_reminder,
    get_users_for_first_lead_reminder,
    get_users_for_second_lead_reminder,
    get_users_for_third_lead_reminder,
    get_users_for_special_offer_reminder
)
from modules.lead_magnet.config import get_lead_magnet_config
from scheduler.reminders.lead_magnet import (
    send_first_lead_reminder,
    send_second_lead_reminder,
    send_third_lead_reminder,
    send_special_offer_reminder
)
from scheduler.reminders.offer_expiration import (
    send_last_call_reminder,
    send_regular_reminder
)
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


async def process_reminders(context):
    """Process all reminders - check database and send messages
    
    Args:
        context: CallbackContext from JobQueue
    """
    db = get_db_session()
    try:
        # Use bot from context
        bot = context.bot
        if bot is None:
            logger.error("Bot is None in process_reminders context")
            return
        
        config = get_lead_magnet_config()
        
        # Lead magnet reminders (after lesson click)
        # Using minutes for testing - all reminders will fire within 1 minute sequentially
        # First reminder (1 minute after click)
        first_lead_offers = get_users_for_first_lead_reminder(
            db,
            hours_after_click=config["first_reminder_hours"]
        )
        logger.info(f"Found {len(first_lead_offers)} users for first lead reminder")
        
        for offer in first_lead_offers:
            user = offer.user
            if user and user.telegram_id:
                # Pass context to enable JobQueue scheduling for special offer
                await send_first_lead_reminder(bot, db, offer, user, context=context)
            else:
                logger.warning(f"Offer {offer.id} has no user or telegram_id")
        
        # Second reminder is now scheduled via JobQueue in send_first_lead_reminder
        # It will be sent automatically 4 hours after first reminder is sent
        # No need to process it here through database queries
        
        # Third reminder is now scheduled via JobQueue in send_second_lead_reminder
        # It will be sent automatically 3 hours after second reminder is sent
        # No need to process it here through database queries
        
        # Fourth reminder is now scheduled via JobQueue in send_third_lead_reminder
        # It will be sent automatically 3 hours after third reminder is sent
        # No need to process it here through database queries
        
        # Offer expiration reminders
        # Get users for last call reminder (24-48 hours before expiration)
        last_call_offers = get_users_for_last_call_reminder(db)
        logger.info(f"Found {len(last_call_offers)} users for last call reminder")
        
        for offer in last_call_offers:
            user = offer.user
            if user and user.telegram_id:
                await send_last_call_reminder(bot, db, offer, user)
            else:
                logger.warning(f"Offer {offer.id} has no user or telegram_id")
        
        # Get users for regular reminder (more than 48 hours before expiration)
        regular_offers = get_users_for_regular_reminder(db, reminder_interval_hours=48)
        logger.info(f"Found {len(regular_offers)} users for regular reminder")
        
        for offer in regular_offers:
            user = offer.user
            if user and user.telegram_id:
                await send_regular_reminder(bot, db, offer, user)
            else:
                logger.warning(f"Offer {offer.id} has no user or telegram_id")
        
        logger.info(f"Reminder processing completed at {datetime.now(timezone.utc)}")
        
    except Exception as e:
        logger.error(f"Error processing reminders: {e}", exc_info=True)
    finally:
        db.close()

