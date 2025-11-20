import logging
import env
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    PreCheckoutQueryHandler,
    MessageHandler,
    filters
)
from modules.init.start import start
from shared.routers.callback_router import route_callback
from shared.constants.callback_register import COMMAND_START
from modules.payment.index import (
    pre_checkout_handler,
    successful_payment_handler,
    get_promocode_conversation_handler
)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


def setup_handlers(application):
    """Register all handlers for the bot"""
    # Command handlers
    application.add_handler(CommandHandler(COMMAND_START, start))
    
    # Promocode conversation handler (must be before CallbackQueryHandler)
    application.add_handler(get_promocode_conversation_handler())
    
    # Callback query handlers
    application.add_handler(CallbackQueryHandler(route_callback))
    
    # Payment handlers
    application.add_handler(PreCheckoutQueryHandler(pre_checkout_handler))
    application.add_handler(MessageHandler(filters.SUCCESSFUL_PAYMENT, successful_payment_handler))


def main():
    """Initialize and run the bot"""
    application = ApplicationBuilder().token(env.TELEGRAM_TOKEN).build()
    
    setup_handlers(application)
    
    application.run_polling()


if __name__ == '__main__':
    main()
