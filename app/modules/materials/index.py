from telegram import Update
from telegram.ext import ContextTypes
from shared.utils.get_back import get_back_keyboard
from modules.materials.config import get_materials_files
import os
import logging

logger = logging.getLogger(__name__)

async def handle_intensive_materials(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle intensive materials callback - send materials to user"""
    query = update.callback_query
    if query:
        await query.answer()
        message = query.message
    else:
        message = update.message
    
    user_id = update.effective_user.id
    
    # No payment status check (Google Sheets removed); allow access
    
    # Get materials files
    materials = get_materials_files()
    
    if not materials:
        text = (
            "📚 Материалы интенсива\n\n"
            "К сожалению, материалы временно недоступны.\n"
            "Мы работаем над их подготовкой и скоро они будут доступны."
        )
        await message.reply_text(text, reply_markup=get_back_keyboard())
        return
    
    # Send message about materials
    text = "📚 Материалы интенсива\n\nОтправляю материалы..."
    await message.reply_text(text)
    
    # Send each material file
    bot = context.bot
    for material in materials:
        file_path = material["path"]
        caption = material.get("caption", "")
        file_type = material.get("type", "document")
        
        try:
            if file_type == "photo":
                with open(file_path, "rb") as f:
                    await bot.send_photo(
                        chat_id=user_id,
                        photo=f,
                        caption=caption if caption else None
                    )
            elif file_type == "video":
                with open(file_path, "rb") as f:
                    await bot.send_video(
                        chat_id=user_id,
                        video=f,
                        caption=caption if caption else None
                    )
            else:  # document
                with open(file_path, "rb") as f:
                    await bot.send_document(
                        chat_id=user_id,
                        document=f,
                        caption=caption if caption else None
                    )
        except FileNotFoundError:
            await bot.send_message(
                chat_id=user_id,
                text=f"⚠️ Файл не найден: {os.path.basename(file_path)}"
            )
        except Exception as e:
            await bot.send_message(
                chat_id=user_id,
                text=f"⚠️ Ошибка при отправке файла: {os.path.basename(file_path)}"
            )
    
    # Send completion message
    completion_text = "✅ Все материалы отправлены!"
    await bot.send_message(chat_id=user_id, text=completion_text, reply_markup=get_back_keyboard())

