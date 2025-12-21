"""
Utility for handling Telegram API errors when sending messages.

This module provides a decorator and helper functions to handle common
Telegram API errors in a consistent way across the application.
"""
from telegram.error import TelegramError, NetworkError, TimedOut, RetryAfter, BadRequest
from typing import Callable, Any, Optional
import logging

logger = logging.getLogger(__name__)


async def send_message_with_error_handling(
    send_func: Callable,
    user_id: int,
    reminder_type: str,
    message_text: Optional[str] = None,
    *args,
    **kwargs
) -> bool:
    """
    Send a Telegram message with comprehensive error handling.
    
    Args:
        send_func: Async function to send message (e.g., bot.send_message)
        user_id: Telegram user ID for logging
        reminder_type: Type of reminder/action for logging (e.g., "first lead reminder")
        message_text: Optional message text for logging length on BadRequest
        *args: Positional arguments to pass to send_func
        **kwargs: Keyword arguments to pass to send_func
    
    Returns:
        True if message was sent successfully, False otherwise
    """
    try:
        await send_func(*args, **kwargs)
        logger.info(f"Sent {reminder_type} to user_id={user_id}")
        return True
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending {reminder_type} to user_id={user_id}: {e}")
        return False
    except RetryAfter as e:
        logger.warning(f"Rate limit sending {reminder_type} to user_id={user_id}: {e}")
        return False
    except BadRequest as e:
        logger.error(f"Bad request sending {reminder_type} to user_id={user_id}: {e}")
        if message_text is not None:
            logger.error(f"Message text length: {len(message_text)}")
        return False
    except TelegramError as e:
        logger.error(f"Failed to send {reminder_type} to user_id={user_id}: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending {reminder_type} to user_id={user_id}: {e}", exc_info=True)
        return False


def handle_telegram_errors(reminder_type: str):
    """
    Decorator for handling Telegram API errors in reminder functions.
    
    Usage:
        @handle_telegram_errors("first lead reminder")
        async def send_first_reminder(bot, db, offer, user):
            await bot.send_message(...)
            return True
    
    Args:
        reminder_type: Type of reminder for logging purposes
    """
    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            # Extract user_id from arguments (usually from 'user' or 'user_id' parameter)
            user_id = None
            if 'user' in kwargs and hasattr(kwargs['user'], 'telegram_id'):
                user_id = kwargs['user'].telegram_id
            elif 'user_id' in kwargs:
                user_id = kwargs['user_id']
            elif len(args) >= 3 and hasattr(args[2], 'telegram_id'):  # Usually (bot, db, user, ...)
                user_id = args[2].telegram_id
            elif len(args) >= 1 and hasattr(args[0], 'telegram_id'):  # Sometimes just user
                user_id = args[0].telegram_id
            
            if user_id is None:
                logger.warning(f"Could not extract user_id for {reminder_type} error handling")
                user_id = "unknown"
            
            try:
                result = await func(*args, **kwargs)
                if result is not False:  # Only log if not explicitly False
                    logger.info(f"Sent {reminder_type} to user_id={user_id}")
                return result
            except (NetworkError, TimedOut) as e:
                logger.warning(f"Network error sending {reminder_type} to user_id={user_id}: {e}")
                return False
            except RetryAfter as e:
                logger.warning(f"Rate limit sending {reminder_type} to user_id={user_id}: {e}")
                return False
            except BadRequest as e:
                logger.error(f"Bad request sending {reminder_type} to user_id={user_id}: {e}")
                # Try to extract message text for logging
                if 'text' in kwargs:
                    logger.error(f"Message text length: {len(kwargs['text'])}")
                return False
            except TelegramError as e:
                logger.error(f"Failed to send {reminder_type} to user_id={user_id}: {e}", exc_info=True)
                return False
            except Exception as e:
                logger.error(f"Unexpected error sending {reminder_type} to user_id={user_id}: {e}", exc_info=True)
                return False
        
        return wrapper
    return decorator

