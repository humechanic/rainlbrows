from telegram import Update
from telegram.ext import ContextTypes
from shared.constants.callback_register import (
    CALLBACK_MENU_MAIN,
    CALLBACK_MENU_DETAILS,
    CALLBACK_MENU_BLOG,
    CALLBACK_MENU_INTENSIVE,
    CALLBACK_PAYMENT_INTENSIVE,
    CALLBACK_MATERIALS_INTENSIVE,
    CALLBACK_GET_LESSON,
    CALLBACK_ADMIN_EXPORT_USERS,
    CALLBACK_ADMIN_EXPORT_OFFERS
)
from modules.main_menu.handler import handle_main_menu
from modules.details.index import handle_details
from modules.blog.index import handle_blog
from modules.intensive.index import handle_intensive
from modules.payment.index import send_intensive_invoice
from modules.materials.index import handle_intensive_materials
from modules.lead_magnet.index import handle_get_lead_magnet
from modules.admin.handlers import handle_export_users, handle_export_offers

# Router mapping callback data to handlers
CALLBACK_ROUTER = {
    CALLBACK_MENU_MAIN: handle_main_menu,
    CALLBACK_MENU_DETAILS: handle_details,
    CALLBACK_MENU_BLOG: handle_blog,
    CALLBACK_MENU_INTENSIVE: handle_intensive,
    CALLBACK_PAYMENT_INTENSIVE: send_intensive_invoice,
    CALLBACK_MATERIALS_INTENSIVE: handle_intensive_materials,
    CALLBACK_GET_LESSON: handle_get_lead_magnet,
    CALLBACK_ADMIN_EXPORT_USERS: handle_export_users,
    CALLBACK_ADMIN_EXPORT_OFFERS: handle_export_offers,
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

