from telegram.error import TelegramError, NetworkError, TimedOut, RetryAfter, BadRequest
from db.session import get_db_session
from db.repository import (
    get_users_for_last_call_reminder,
    get_users_for_regular_reminder,
    update_reminder_sent,
    get_users_for_first_lead_reminder,
    get_users_for_second_lead_reminder,
    get_users_for_third_lead_reminder,
    mark_first_reminder_sent,
    mark_second_reminder_sent
)
from modules.lead_magnet.config import get_lead_magnet_config
from shared.utils.get_lead_reminder_keyboards import (
    get_watch_lesson_keyboard,
    get_second_reminder_keyboard,
    get_third_reminder_keyboard,
    get_last_call_reminder_keyboard
)
import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


async def send_last_call_reminder(bot, db, offer, user):
    """Send 'last call' reminder message"""
    expiration_date = offer.offer_expiration_date.strftime("%d.%m.%Y в %H:%M")
    text = (
        f"⚠️ Внимание! Ваше специальное предложение истекает завтра в {expiration_date}!\n\n"
        f"Не упустите возможность воспользоваться выгодным предложением!"
    )
    
    try:
        keyboard = get_last_call_reminder_keyboard()
        await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            reply_markup=keyboard
        )
        update_reminder_sent(db, offer.id, reminder_type='last_call')
        logger.info(f"Sent last call reminder to user_id={user.telegram_id}")
        return True
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending last call reminder to user_id={user.telegram_id}: {e}")
        return False
    except RetryAfter as e:
        logger.warning(f"Rate limit sending last call reminder to user_id={user.telegram_id}: {e}")
        return False
    except BadRequest as e:
        logger.error(f"Bad request sending last call reminder to user_id={user.telegram_id}: {e}")
        return False
    except TelegramError as e:
        logger.error(f"Failed to send last call reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending last call reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False


async def send_regular_reminder(bot, db, offer, user):
    """Send regular reminder message"""
    expiration_date = offer.offer_expiration_date.strftime("%d.%m.%Y в %H:%M")
    text = (
        f"💡 Не забудьте! Ваше специальное предложение все еще ждет вас.\n\n"
        f"⏰ Действует до: {expiration_date}\n\n"
        f"Воспользуйтесь выгодным предложением пока оно активно!"
    )
    
    try:
        await bot.send_message(chat_id=user.telegram_id, text=text)
        update_reminder_sent(db, offer.id, reminder_type=None)
        logger.info(f"Sent regular reminder to user_id={user.telegram_id}")
        return True
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending regular reminder to user_id={user.telegram_id}: {e}")
        return False
    except RetryAfter as e:
        logger.warning(f"Rate limit sending regular reminder to user_id={user.telegram_id}: {e}")
        return False
    except BadRequest as e:
        logger.error(f"Bad request sending regular reminder to user_id={user.telegram_id}: {e}")
        return False
    except TelegramError as e:
        logger.error(f"Failed to send regular reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending regular reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False


async def send_first_lead_reminder(bot, db, offer, user):
    """Send watch lesson reminder (1 hour after lesson click)"""
    text = (
        "Коллеги, не забывайте посмотреть урок “ТОП 3 ошибки в продажах бьюти мастера\"\n\n"
        "Что разобрали?\n\n"
        "▪️ почему клиенты не записываются? ТОП ошибок, о которых никто не говорит\n\n"
        "▪️ реальные примеры из практики для любой бьюти-ниши\n\n"
        "▪️ как привести к покупке через 5 минут после подписки\n\n"
        "🔥рекомендации, которые можно внедрить сразу в ваш инстаграм\n\n"
        "А также рассказала про свой интенсив \"Продажи бьюти-мастера\" и бонусы для участников интенсива❤️\n\n"
        f"Ссылка на урок: {get_lead_magnet_config()['youtube_url']}"
    )
    
    try:
        keyboard = get_watch_lesson_keyboard()
        await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            reply_markup=keyboard
        )
        mark_first_reminder_sent(db, offer.id)
        logger.info(f"Sent first lead reminder to user_id={user.telegram_id}")
        return True
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending first lead reminder to user_id={user.telegram_id}: {e}")
        return False
    except RetryAfter as e:
        logger.warning(f"Rate limit sending first lead reminder to user_id={user.telegram_id}: {e}")
        return False
    except BadRequest as e:
        logger.error(f"Bad request sending first lead reminder to user_id={user.telegram_id}: {e}")
        return False
    except TelegramError as e:
        logger.error(f"Failed to send first lead reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending first lead reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False


async def send_second_lead_reminder(bot, db, offer, user):
    """Send special price reminder (second touch)"""
    text = (
        "❓ <b>ТОП-4 вопроса об интенсиве \"Продажи бьюти-мастера\"</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
        
        "🔹 <b>Для какой бьюти ниши подойдет интенсив?</b>\n"
        "   Интенсив подходит для любой ниши: брови, перманент, массаж, ламинирование ресниц, "
        "косметология, подология, маникюр, кератин - примеры и инструменты в уроках можно "
        "адаптировать под любую нишу.\n\n"
        
        "🔹 <b>Смогу ли я проходить интенсив, если у меня плотный график?</b>\n"
        "   Да, уроки интенсива в записи, можно просматривать их и выполнять рекомендации в "
        "любое удобное для вас время.\n\n"
        
        "🔹 <b>Хочу начать обучать, поможет ли мне интенсив?</b>\n"
        "   Да, уроки в интенсиве построены на базовых знаниях маркетинга и продаж, поэтому "
        "вы с легкостью сможете их адаптировать для вашего будущего курса.\n\n"
        
        "🔹 <b>Смогу ли я задать вопросы по своему инстаграм автору интенсива?</b>\n"
        "   Да, после просмотра интенсива вы сможете задать вопросы в отдельный чат, Анна "
        "дает обратную связь в чате и также проводит прямые эфиры с разбором популярных вопросов.\n\n"
        
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "💫 <i>Почему бы не начать Новый год по новому? Еще и с поддержкой и рекомендациями от меня.</i>\n\n"
        "🔥 <b>Смотри урок {get_lead_magnet_config()['youtube_url']}, там есть промокод на участие</b>"
    )
    
    try:
        keyboard = get_second_reminder_keyboard()
        await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
        )
        mark_second_reminder_sent(db, offer.id)
        logger.info(f"Sent second lead reminder to user_id={user.telegram_id}")
        return True
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending second lead reminder to user_id={user.telegram_id}: {e}")
        return False
    except RetryAfter as e:
        logger.warning(f"Rate limit sending second lead reminder to user_id={user.telegram_id}: {e}")
        return False
    except BadRequest as e:
        logger.error(f"Bad request sending second lead reminder to user_id={user.telegram_id}: {e}")
        logger.error(f"Message text length: {len(text)}")
        return False
    except TelegramError as e:
        logger.error(f"Failed to send second lead reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending second lead reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False

async def send_third_lead_reminder(bot, db, offer, user):
    """Send final push special offer reminder (3 hours after second reminder)"""
    text = (
        "🔔 <b>Важно!</b>\n"
        "Скоро спецпредложение пропадет\n\n"
        
        "Успей:\n\n"
        
        "▪️ Забрать место на курсе с выгодой (без промокода цена будет выше)\n\n"
        
        "▪️ Получить бонусы:\n\n"
        
        "- урок «Нейросети для бьюти мастера» - как создать контент без моделей, с 0 и оживить фото "
        "(практический урок от приглашенного эксперта Александры Легович)\n\n"
        
        "- готовый контент-план с идеями, который можно адаптировать под любой месяц и нишу\n\n"

    )
    
    try:
        keyboard = get_third_reminder_keyboard()
        await bot.send_message(
            chat_id=user.telegram_id,
            text=text,
            parse_mode='HTML',
            reply_markup=keyboard
        )
        update_reminder_sent(db, offer.id, reminder_type="third_lead")
        logger.info(f"Sent third lead reminder to user_id={user.telegram_id}")
        return True
    except (NetworkError, TimedOut) as e:
        logger.warning(f"Network error sending third lead reminder to user_id={user.telegram_id}: {e}")
        return False
    except RetryAfter as e:
        logger.warning(f"Rate limit sending third lead reminder to user_id={user.telegram_id}: {e}")
        return False
    except BadRequest as e:
        logger.error(f"Bad request sending third lead reminder to user_id={user.telegram_id}: {e}")
        logger.error(f"Message text length: {len(text)}")
        return False
    except TelegramError as e:
        logger.error(f"Failed to send third lead reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False
    except Exception as e:
        logger.error(f"Unexpected error sending third lead reminder to user_id={user.telegram_id}: {e}", exc_info=True)
        return False


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
                await send_first_lead_reminder(bot, db, offer, user)
            else:
                logger.warning(f"Offer {offer.id} has no user or telegram_id")
        
        # Second reminder (2 minutes after click = 1 minute after first)
        second_lead_offers = get_users_for_second_lead_reminder(
            db,
            hours_after_click=config["second_reminder_hours"]
        )
        logger.info(f"Found {len(second_lead_offers)} users for second lead reminder")
        
        for offer in second_lead_offers:
            user = offer.user
            if user and user.telegram_id:
                await send_second_lead_reminder(bot, db, offer, user)
            else:
                logger.warning(f"Offer {offer.id} has no user or telegram_id")
        
        # Third reminder (1 minute after second reminder)
        third_lead_offers = get_users_for_third_lead_reminder(
            db,
            hours_after_second=config["third_reminder_after_second_hours"]
        )
        logger.info(f"Found {len(third_lead_offers)} users for third lead reminder")
        
        for offer in third_lead_offers:
            user = offer.user
            if user and user.telegram_id:
                await send_third_lead_reminder(bot, db, offer, user)
            else:
                logger.warning(f"Offer {offer.id} has no user or telegram_id")
        
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


if __name__ == "__main__":
    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )
    
    # Run reminder processing
    import asyncio
    asyncio.run(process_reminders())

