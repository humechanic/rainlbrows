import logging
from telegram import User
from db.session import get_db_session
from db.repository import get_or_create_user, create_or_update_offer, log_pay_click

logger = logging.getLogger(__name__)


def track_start_analytics(user: User, offer_expiration_days: int) -> None:
    """Persist user and offer data for analytics purposes."""
    db = get_db_session()
    try:
        db_user = get_or_create_user(
            db=db,
            telegram_id=user.id,
            nickname=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_premium=bool(getattr(user, "is_premium", False) or False),
        )

        create_or_update_offer(
            db=db,
            user_id=db_user.id,
            expiration_days=offer_expiration_days,
        )
    except Exception as error:
        logger.error("Failed to track start analytics", exc_info=True)
        raise error
    finally:
        db.close()


def track_pay_click(user: User, source: str | None = None) -> None:
    """Persist user for analytics when pay/оплатить button is clicked."""
    db = get_db_session()
    try:
        db_user = get_or_create_user(
            db=db,
            telegram_id=user.id,
            nickname=user.username,
            first_name=user.first_name,
            last_name=user.last_name,
            is_premium=bool(getattr(user, "is_premium", False) or False),
        )
        log_pay_click(db=db, user_id=db_user.id, source=source)
    except Exception as error:
        logger.error("Failed to track pay click", exc_info=True)
        raise error
    finally:
        db.close()
