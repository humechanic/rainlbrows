from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
import env
import logging

logger = logging.getLogger(__name__)
from modules.payment.promocodes import (
    is_valid_promocode,
    get_discount_value,
    calculate_discount_amount,
    calculate_final_price,
    is_percentage_discount
)
from shared.utils.get_intensive_keyboard import get_intensive_keyboard
from shared.constants.callback_register import CALLBACK_PROMOCODE
from modules.main_menu.index import get_main_menu_keyboard

# Payment configuration
PAYMENT_PROVIDER_TOKEN = env.PAYMENT_PROVIDER_TOKEN
INTENSIVE_PRICE = 35000  # Price in cents (100.00 currency units)
INTENSIVE_CURRENCY = "BYN"
INTENSIVE_TITLE = "Интенсив по продажам для бьюти-мастера"
INTENSIVE_DESCRIPTION = "Запись на интенсив по продажам для бьюти-мастера"
INTENSIVE_PAYLOAD = "intensive_payment"

# Conversation states
WAITING_FOR_PROMOCODE = 1

async def start_promocode_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start promocode input conversation"""
    query = update.callback_query
    if query:
        await query.answer()
        text = "Введите промокод:"
        await query.message.reply_text(text)
    return WAITING_FOR_PROMOCODE

async def process_promocode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Process entered promocode"""
    promocode = update.message.text.strip()
    user_id = update.effective_user.id
    
    # Get database session to check offer expiration for "УРОК" promocode
    from db.session import get_db_session
    from db.repository import get_or_create_user
    
    db = get_db_session()
    try:
        # Get or create user to get user_id for offer check
        db_user = get_or_create_user(
            db=db,
            telegram_id=user_id,
            nickname=update.effective_user.username,
            first_name=update.effective_user.first_name,
            last_name=update.effective_user.last_name,
            is_premium=bool(getattr(update.effective_user, 'is_premium', False) or False)
        )
        
        # Check if promocode is valid (including offer expiration check for "УРОК")
        if is_valid_promocode(promocode, user_id=db_user.id, db_session=db):
            discount_value = get_discount_value(promocode)
            discount_amount = calculate_discount_amount(INTENSIVE_PRICE, discount_value)
            final_price = calculate_final_price(INTENSIVE_PRICE, discount_value)
            
            # Store discount in user_data
            context.user_data['discount_value'] = discount_value
            context.user_data['promocode'] = promocode.upper()
            
            # Convert to currency units for display
            discount_display = discount_amount / 100
            final_price_display = final_price / 100
            
            # Build discount description
            if is_percentage_discount(discount_value):
                discount_desc = f"📊 Скидка: {discount_value}"
            else:
                discount_desc = f"📊 Скидка: {discount_display:.2f} {INTENSIVE_CURRENCY}"
            
            text = (
                f"✅ Промокод '{promocode.upper()}' применен!\n\n"
                f"💰 Экономия: {discount_display:.2f} {INTENSIVE_CURRENCY}\n"
                f"💵 Цена со скидкой: {final_price_display:.2f} {INTENSIVE_CURRENCY}\n"
                f"{discount_desc}"
            )
            await update.message.reply_text(text, reply_markup=get_intensive_keyboard())
        else:
            # Check if it's "УРОК" promocode that expired
            if promocode.upper() == "УРОК":
                text = (
                    "❌ Промокод 'УРОК' больше не действителен.\n\n"
                    "⏰ Срок действия специального предложения истек.\n"
                    "Попробуйте другой промокод или вернитесь назад."
                )
            else:
                text = "❌ Промокод не существует. Попробуйте еще раз или вернитесь назад."
            await update.message.reply_text(text, reply_markup=get_intensive_keyboard())
    except Exception as e:
        logger.error(f"Error processing promocode: {e}", exc_info=True)
        text = "❌ Произошла ошибка при проверке промокода. Попробуйте еще раз."
        await update.message.reply_text(text, reply_markup=get_intensive_keyboard())
    finally:
        db.close()
    
    return ConversationHandler.END

async def cancel_promocode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel promocode input and return to intensive page"""
    text = "Ввод промокода отменен."
    
    # Handle both callback query and message
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_text(text, reply_markup=get_intensive_keyboard())
    else:
        await update.message.reply_text(text, reply_markup=get_intensive_keyboard())
    
    return ConversationHandler.END

async def send_intensive_invoice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send invoice for intensive payment"""
    query = update.callback_query
    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message
    
    # Get discount from user_data if exists
    discount_value = context.user_data.get('discount_value', '')
    if discount_value:
        final_price = calculate_final_price(INTENSIVE_PRICE, discount_value)
    else:
        final_price = INTENSIVE_PRICE
    
    # Build description with discount info
    description = INTENSIVE_DESCRIPTION
    if discount_value:
        promocode = context.user_data.get('promocode', '')
        if is_percentage_discount(discount_value):
            description += f"\n\nПромокод: {promocode}\nСкидка: {discount_value}"
        else:
            discount_amount = calculate_discount_amount(INTENSIVE_PRICE, discount_value)
            discount_display = discount_amount / 100
            description += f"\n\nПромокод: {promocode}\nСкидка: {discount_display:.2f} {INTENSIVE_CURRENCY}"
    
    # Create price label - use simple label without special characters
    # Note: If Telegram shows USD instead of BYN, it may be because:
    # 1. BYN is not supported in test mode by the payment provider
    # 2. The payment provider defaults to USD in test mode
    # 3. Telegram Bot API may not fully support BYN in test mode
    # In production mode with a real payment provider, BYN should work correctly
    price_label = "Интенсив"
    prices = [LabeledPrice(price_label, final_price)]
    
    await message.reply_invoice(
        title=INTENSIVE_TITLE,
        description=description,
        payload=INTENSIVE_PAYLOAD,
        provider_token=PAYMENT_PROVIDER_TOKEN,
        currency=INTENSIVE_CURRENCY,  # BYN - may show as USD in test mode
        prices=prices,
    )

async def pre_checkout_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle pre-checkout query - approve payment"""
    query = update.pre_checkout_query
    if not query:
        logger.warning("pre_checkout_handler called but update.pre_checkout_query is None")
        return
    
    try:
        # PreCheckoutQuery uses invoice_payload, not payload
        invoice_payload = getattr(query, 'invoice_payload', None)
        if not invoice_payload:
            logger.warning(f"PreCheckoutQuery has no invoice_payload attribute. Query: {query}")
            await query.answer(ok=False, error_message="Invalid payment request")
            return
        
        if invoice_payload == INTENSIVE_PAYLOAD:
            await query.answer(ok=True)
            logger.info(f"Payment approved for invoice_payload: {invoice_payload}")
        else:
            logger.warning(f"Unknown payment invoice_payload: {invoice_payload}")
            await query.answer(ok=False, error_message="Unknown payment payload")
    except AttributeError as e:
        logger.error(f"AttributeError in pre_checkout_handler: {e}, query: {query}")
        try:
            await query.answer(ok=False, error_message="Payment processing error")
        except:
            pass
    except Exception as e:
        logger.error(f"Error in pre_checkout_handler: {e}", exc_info=True)
        # Try to answer query to prevent loading indicator
        try:
            await query.answer(ok=False, error_message="Payment processing error")
        except:
            pass

async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful payment"""
    payment = update.message.successful_payment
    if payment.invoice_payload == INTENSIVE_PAYLOAD:
        user = update.effective_user
        user_id = user.id
        username = user.username or user.first_name or ""
        
        # Cancel scheduled reminders (target action-2 performed)
        try:
            from scheduler.job_queue_reminders import cancel_lead_reminders
            cancel_lead_reminders(context, user_id)
            logger.info(f"Cancelled lead reminders for user_id={user_id} after successful payment")
        except Exception as cancel_error:
            logger.warning(f"Error cancelling reminders for user_id={user_id}: {cancel_error}")
        
        # Get payment amount
        payment_amount = f"{payment.total_amount / 100:.2f} {payment.currency}"
        
        # Congratulate user
        text = (
            "🎉 Поздравляем! Оплата прошла успешно!\n\n"
            "✅ Ваша запись на интенсив подтверждена.\n"
            "📚 Теперь у вас есть доступ к материалам интенсива.\n\n"
            "Мы свяжемся с вами в ближайшее время."
        )
        await update.message.reply_text(
            text, 
            reply_markup=get_main_menu_keyboard(has_paid=True, user_id=user_id)
        )
        
        # Clear discount data after successful payment - reset promocode
        if 'discount_value' in context.user_data:
            del context.user_data['discount_value']
        if 'promocode' in context.user_data:
            del context.user_data['promocode']

async def failed_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle failed payment"""
    text = (
        "❌ К сожалению, оплата не прошла.\n\n"
        "Возможные причины:\n"
        "• Недостаточно средств на карте\n"
        "• Проблемы с банком\n"
        "• Отмена платежа\n\n"
        "Попробуйте оплатить снова или вернитесь в главное меню."
    )
    
    # Create keyboard with back to main menu button
    from telegram import InlineKeyboardButton, InlineKeyboardMarkup
    from shared.constants.callback_register import CALLBACK_MENU_MAIN, CALLBACK_MENU_INTENSIVE, BUTTON_TEXT_BACK
    
    keyboard = [
        [InlineKeyboardButton("Попробовать снова", callback_data=CALLBACK_MENU_INTENSIVE)],
        [InlineKeyboardButton(BUTTON_TEXT_BACK, callback_data=CALLBACK_MENU_MAIN)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(text, reply_markup=reply_markup)

def get_promocode_conversation_handler():
    """Create and return ConversationHandler for promocode input"""
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(start_promocode_input, pattern=f"^{CALLBACK_PROMOCODE}$")],
        states={
            WAITING_FOR_PROMOCODE: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, process_promocode)
            ],
        },
        fallbacks=[
            # Cancel on any callback query (user pressed any button)
            CallbackQueryHandler(cancel_promocode),
            # Cancel on any command
            MessageHandler(filters.COMMAND, cancel_promocode)
        ],
    )

