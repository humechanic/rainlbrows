from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from datetime import datetime, timedelta, timezone
from db.models import User, Offer, PayClick
import logging

logger = logging.getLogger(__name__)


def get_or_create_user(
    db: Session,
    telegram_id: int,
    nickname: str = None,
    first_name: str = None,
    last_name: str = None,
    is_premium: bool = False
) -> User:
    """Get existing user or create new one"""
    # Ensure is_premium is always a boolean, never None
    is_premium = bool(is_premium) if is_premium is not None else False
    
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    
    if user:
        # Update user info if provided
        if nickname is not None:
            user.nickname = nickname
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        user.is_premium_tg_user = is_premium
        db.commit()
        db.refresh(user)
        return user
    
    # Create new user
    user = User(
        telegram_id=telegram_id,
        nickname=nickname,
        first_name=first_name,
        last_name=last_name,
        is_premium_tg_user=is_premium
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    logger.info(f"Created new user: telegram_id={telegram_id}")
    return user


def create_or_update_offer(
    db: Session,
    user_id: int,
    expiration_days: int = 7
) -> Offer:
    """Create new offer or update existing active offer for user"""
    # Check if user has active offer
    active_offer = db.query(Offer).filter(
        and_(
            Offer.user_id == user_id,
            Offer.is_active == True
        )
    ).first()
    
    if active_offer:
        # Update existing offer expiration date
        active_offer.offer_expiration_date = datetime.now(timezone.utc) + timedelta(days=expiration_days)
        active_offer.last_reminder_sent = None  # Reset reminder
        active_offer.reminder_type = None
        db.commit()
        db.refresh(active_offer)
        logger.info(f"Updated offer for user_id={user_id}")
        return active_offer
    
    # Create new offer
    offer = Offer(
        user_id=user_id,
        offer_expiration_date=datetime.now(timezone.utc) + timedelta(days=expiration_days),
        last_reminder_sent=None,
        is_active=True,
        reminder_type=None
    )
    db.add(offer)
    db.commit()
    db.refresh(offer)
    logger.info(f"Created new offer for user_id={user_id}, expires in {expiration_days} days")
    return offer


def get_users_for_last_call_reminder(db: Session) -> list[Offer]:
    """Get users who need 'last call' reminder (24-48 hours before expiration)"""
    now = datetime.now(timezone.utc)
    tomorrow = now + timedelta(hours=24)
    day_after_tomorrow = now + timedelta(hours=48)
    
    offers = db.query(Offer).filter(
        and_(
            Offer.offer_expiration_date >= tomorrow,
            Offer.offer_expiration_date <= day_after_tomorrow,
            Offer.is_active == True,
            Offer.reminder_type != 'last_call'  # Not already sent
        )
    ).all()
    
    return offers


def get_users_for_regular_reminder(db: Session, reminder_interval_hours: int = 48) -> list[Offer]:
    """Get users who need regular reminder (more than 48 hours before expiration, last reminder was more than interval ago)"""
    now = datetime.now(timezone.utc)
    future_threshold = now + timedelta(hours=48)  # More than 48 hours before expiration
    last_reminder_threshold = now - timedelta(hours=reminder_interval_hours)
    
    offers = db.query(Offer).filter(
        and_(
            Offer.offer_expiration_date > future_threshold,
            Offer.is_active == True,
            # Either no reminder sent, or last reminder was more than interval ago
            or_(
                Offer.last_reminder_sent == None,
                Offer.last_reminder_sent < last_reminder_threshold
            ),
            Offer.reminder_type != 'last_call'  # Not a last call reminder
        )
    ).all()
    
    return offers


def update_reminder_sent(db: Session, offer_id: int, reminder_type: str = None):
    """Update last_reminder_sent timestamp for offer"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if offer:
        offer.last_reminder_sent = datetime.now(timezone.utc)
        if reminder_type:
            offer.reminder_type = reminder_type
        db.commit()
        logger.info(f"Updated reminder_sent for offer_id={offer_id}, type={reminder_type}")


def mark_lesson_clicked(db: Session, user_id: int):
    """Mark that user clicked 'забрать урок' button"""
    # Get user's active offer
    offer = db.query(Offer).filter(
        and_(
            Offer.user_id == user_id,
            Offer.is_active == True
        )
    ).first()
    
    if offer:
        offer.lesson_clicked_at = datetime.now(timezone.utc)
        db.commit()
        logger.info(f"Marked lesson clicked for user_id={user_id}, offer_id={offer.id}")
        return offer
    else:
        logger.warning(f"No active offer found for user_id={user_id}")
        return None


def get_offer_by_id(db: Session, offer_id: int) -> Offer:
    """Get offer by ID"""
    return db.query(Offer).filter(Offer.id == offer_id).first()


def get_active_offer_for_user(db: Session, user_id: int) -> Offer:
    """Get active offer for user by user_id (not telegram_id)"""
    return db.query(Offer).filter(
        and_(
            Offer.user_id == user_id,
            Offer.is_active == True
        )
    ).first()


def get_users_for_first_lead_reminder(db: Session, hours_after_click: int = 1, minutes_after_click: int = None) -> list[Offer]:
    """Get users who need first lead magnet reminder (1 hour after clicking lesson)
    
    Args:
        hours_after_click: Hours after click (default: 1)
        minutes_after_click: Minutes after click (for testing, overrides hours_after_click if provided)
    """
    now = datetime.now(timezone.utc)
    if minutes_after_click is not None:
        threshold = now - timedelta(minutes=minutes_after_click)
    else:
        threshold = now - timedelta(hours=hours_after_click)
    
    offers = db.query(Offer).filter(
        and_(
            Offer.lesson_clicked_at != None,
            Offer.lesson_clicked_at <= threshold,
            Offer.first_reminder_sent == None,  # Not sent yet
            Offer.is_active == True
        )
    ).all()
    
    return offers


def get_users_for_second_lead_reminder(db: Session, hours_after_click: int = 12, minutes_after_click: int = None) -> list[Offer]:
    """Get users who need second lead magnet reminder (12 hours after clicking lesson)
    
    Args:
        hours_after_click: Hours after click (default: 12)
        minutes_after_click: Minutes after click (for testing, overrides hours_after_click if provided)
    """
    now = datetime.now(timezone.utc)
    if minutes_after_click is not None:
        threshold = now - timedelta(minutes=minutes_after_click)
    else:
        threshold = now - timedelta(hours=hours_after_click)
    
    offers = db.query(Offer).filter(
        and_(
            Offer.lesson_clicked_at != None,
            Offer.lesson_clicked_at <= threshold,
            Offer.first_reminder_sent != None,  # First reminder already sent
            Offer.second_reminder_sent == None,  # Second not sent yet
            Offer.is_active == True
        )
    ).all()
    
    return offers


def get_users_for_third_lead_reminder(db: Session, hours_after_second: int = 3, minutes_after_second: int = None) -> list[Offer]:
    """Get users who need third lead magnet reminder (hours after second reminder)
    
    Args:
        hours_after_second: Hours after second reminder (default: 3)
        minutes_after_second: Minutes after second reminder (for testing, overrides hours_after_second if provided)
    """
    now = datetime.now(timezone.utc)
    if minutes_after_second is not None:
        threshold = now - timedelta(minutes=minutes_after_second)
    else:
        threshold = now - timedelta(hours=hours_after_second)
    
    offers = db.query(Offer).filter(
        and_(
            Offer.lesson_clicked_at != None,
            Offer.second_reminder_sent != None,
            Offer.second_reminder_sent <= threshold,
            Offer.reminder_type != "third_lead",
            Offer.is_active == True
        )
    ).all()
    
    return offers


def mark_first_reminder_sent(db: Session, offer_id: int):
    """Mark first lead magnet reminder as sent"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if offer:
        offer.first_reminder_sent = datetime.now(timezone.utc)
        db.commit()
        logger.info(f"Marked first reminder sent for offer_id={offer_id}")


def mark_second_reminder_sent(db: Session, offer_id: int):
    """Mark second lead magnet reminder as sent"""
    offer = db.query(Offer).filter(Offer.id == offer_id).first()
    if offer:
        offer.second_reminder_sent = datetime.now(timezone.utc)
        db.commit()
        logger.info(f"Marked second reminder sent for offer_id={offer_id}")


def get_users_for_special_offer_reminder(db: Session, hours_after_click: int = 24, minutes_after_click: int = None) -> list[Offer]:
    """Get users who need special offer reminder (24 hours after lesson click)
    
    Args:
        hours_after_click: Hours after lesson click (default: 24)
        minutes_after_click: Minutes after lesson click (for testing, overrides hours_after_click if provided)
    """
    now = datetime.now(timezone.utc)
    if minutes_after_click is not None:
        threshold = now - timedelta(minutes=minutes_after_click)
    else:
        threshold = now - timedelta(hours=hours_after_click)
    
    offers = db.query(Offer).filter(
        and_(
            Offer.lesson_clicked_at != None,
            Offer.lesson_clicked_at <= threshold,
            Offer.reminder_type != "special_offer",  # Not already sent
            Offer.is_active == True
        )
    ).all()
    
    return offers


def log_pay_click(db: Session, user_id: int, source: str | None = None) -> PayClick:
    """Create pay click analytics record"""
    pay_click = PayClick(
        user_id=user_id,
        source=source
    )
    db.add(pay_click)
    db.commit()
    db.refresh(pay_click)
    logger.info(f"Logged pay click: user_id={user_id}, source={source}")
    return pay_click

