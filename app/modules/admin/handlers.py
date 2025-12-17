"""
Admin handlers for callback queries
"""
from telegram import Update, InputFile
from telegram.ext import ContextTypes
from telegram.error import TelegramError
from modules.admin.export import export_users_to_pdf, export_offers_to_pdf
import logging

logger = logging.getLogger(__name__)


async def handle_export_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle export users to PDF"""
    query = update.callback_query
    if query:
        await query.answer()
    
    try:
        status_msg = await query.message.reply_text("⏳ Генерирую PDF с базой пользователей...")
        
        # Generate PDF
        pdf_buffer = export_users_to_pdf()
        
        # Create InputFile from BytesIO
        pdf_file = InputFile(pdf_buffer, filename=f"users_export_{update.effective_user.id}.pdf")
        
        # Send PDF as document
        await context.bot.send_document(
            chat_id=update.effective_user.id,
            document=pdf_file,
            caption="📄 База пользователей"
        )
        
        # Delete status message
        try:
            await status_msg.delete()
        except:
            pass
        
        logger.info(f"Exported users PDF for admin user_id={update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error exporting users: {e}", exc_info=True)
        error_text = "❌ Произошла ошибка при выгрузке базы пользователей."
        try:
            if query:
                await query.message.reply_text(error_text)
        except:
            pass


async def handle_export_offers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle export offers to PDF"""
    query = update.callback_query
    if query:
        await query.answer()
    
    try:
        status_msg = await query.message.reply_text("⏳ Генерирую PDF с базой предложений...")
        
        # Generate PDF
        pdf_buffer = export_offers_to_pdf()
        
        # Create InputFile from BytesIO
        pdf_file = InputFile(pdf_buffer, filename=f"offers_export_{update.effective_user.id}.pdf")
        
        # Send PDF as document
        await context.bot.send_document(
            chat_id=update.effective_user.id,
            document=pdf_file,
            caption="📄 База предложений"
        )
        
        # Delete status message
        try:
            await status_msg.delete()
        except:
            pass
        
        logger.info(f"Exported offers PDF for admin user_id={update.effective_user.id}")
        
    except Exception as e:
        logger.error(f"Error exporting offers: {e}", exc_info=True)
        error_text = "❌ Произошла ошибка при выгрузке базы предложений."
        try:
            if query:
                await query.message.reply_text(error_text)
        except:
            pass

