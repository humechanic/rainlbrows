from telegram import Update, LabeledPrice
from telegram.ext import ContextTypes, ConversationHandler, CallbackQueryHandler, MessageHandler, filters
import env
from modules.payment.promocodes import (
    is_valid_promocode,
    get_discount_value,
    calculate_discount_amount,
    calculate_final_price,
    is_percentage_discount
)
from shared.utils.get_intensive_keyboard import get_intensive_keyboard
from shared.constants.callback_register import CALLBACK_PROMOCODE

# Payment configuration
PAYMENT_PROVIDER_TOKEN = getattr(env, 'PAYMENT_PROVIDER_TOKEN', 'TEST_PAYMENT_PROVIDER_TOKEN')
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
    
    if is_valid_promocode(promocode):
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
        text = "❌ Промокод не существует. Попробуйте еще раз или вернитесь назад."
        await update.message.reply_text(text, reply_markup=get_intensive_keyboard())
    
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
    if query.payload == INTENSIVE_PAYLOAD:
        await query.answer(ok=True)
    else:
        await query.answer(ok=False, error_message="Unknown payment payload")

async def successful_payment_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle successful payment"""
    payment = update.message.successful_payment
    if payment.invoice_payload == INTENSIVE_PAYLOAD:
        text = "Спасибо за оплату! Ваша запись на интенсив подтверждена. Мы свяжемся с вами в ближайшее время."
        await update.message.reply_text(text)
        # Clear discount data after successful payment - reset promocode
        if 'discount_value' in context.user_data:
            del context.user_data['discount_value']
        if 'promocode' in context.user_data:
            del context.user_data['promocode']

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

