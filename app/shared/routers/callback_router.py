from telegram import Update
from telegram.ext import ContextTypes
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    CALLBACK_MENU_DETAILS,
    CALLBACK_MENU_BLOG,
    CALLBACK_MENU_INTENSIVE
)
from modules.main_menu.handler import handle_main_menu
from modules.details.index import handle_details
from modules.blog.index import handle_blog
from modules.intensive.index import handle_intensive

# Router mapping callback data to handlers
CALLBACK_ROUTER = {
    CALLBACK_MENU_MAIN: handle_main_menu,
    CALLBACK_MENU_DETAILS: handle_details,
    CALLBACK_MENU_BLOG: handle_blog,
    CALLBACK_MENU_INTENSIVE: handle_intensive,
}

async def route_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Centralized router for callback queries"""
    query = update.callback_query
    if not query:
        return
    
    callback_data = query.data
    
    # Get handler from router
    handler = CALLBACK_ROUTER.get(callback_data)
    
    if handler:
        await handler(update, context)
    else:
        # Unknown callback data - answer to prevent loading indicator
        await query.answer()

