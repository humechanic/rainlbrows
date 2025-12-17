"""
Configuration for lesson content and reminder intervals
You can use either YouTube link or Telegram video
"""

# Reminder intervals (in hours)
FIRST_REMINDER_HOURS = 1  # Watch lesson reminder after 1 hour
SECOND_REMINDER_HOURS = 2  # Special price reminder after 2 hours (1h + 1h)
THIRD_REMINDER_AFTER_SECOND_HOURS = 3  # Final push 3 hours after second reminder

# Testing intervals (in minutes) - for development/testing
FIRST_REMINDER_MINUTES = 1  # First reminder after 1 minute (for testing)
LAST_CALL_REMINDER_MINUTES = 2  # Last call reminder after 2 minutes (for testing)

# Option 1: YouTube link (recommended - simple and doesn't require file storage)
ERROR_3_STEP_LESSON_YOUTUBE_URL = "https://www.youtube.com/watch?v=A2z9Ug3K4p0"
# Or use short link: LESSON_YOUTUBE_URL = "https://youtu.be/YOUR_VIDEO_ID"

# Option 2: Telegram video (use file_id if video is already uploaded to Telegram)
# To get file_id: send video to your bot, then check update.message.video.file_id
LESSON_TELEGRAM_VIDEO_FILE_ID = None  # Example: "BAACAgIAAxkBAAIBY2..." 

# Option 3: Local video file path (video will be uploaded from disk)
LESSON_VIDEO_FILE_PATH = None  # Example: "lessons/lesson_video.mp4"

# Lesson description text
LESSON_DESCRIPTION = (
    "🎥 Урок: 3 простых шага для привлечения клиентов\n\n"
    "В этом уроке ты узнаешь:\n"
    "• Как заполнить клиентскую запись\n"
    "• Как не вести сторис 24/7\n"
    "• Как сделать так, чтобы клиенты сами захотели к вам прийти"
)

# Contact username for questions
CONTACT_USERNAME = "anna_rainl"


def get_lead_magnet_config():
    """Get lesson configuration"""
    return {
        "youtube_url": ERROR_3_STEP_LESSON_YOUTUBE_URL,
        "telegram_file_id": LESSON_TELEGRAM_VIDEO_FILE_ID,
        "video_file_path": LESSON_VIDEO_FILE_PATH,
        "description": LESSON_DESCRIPTION,
        "first_reminder_hours": FIRST_REMINDER_HOURS,
        "second_reminder_hours": SECOND_REMINDER_HOURS,
        "third_reminder_after_second_hours": THIRD_REMINDER_AFTER_SECOND_HOURS,
        "third_reminder_hours": THIRD_REMINDER_AFTER_SECOND_HOURS,
        "last_call_reminder_minutes": LAST_CALL_REMINDER_MINUTES,
        "contact_username": CONTACT_USERNAME
    }

