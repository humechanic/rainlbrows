"""
Migration script to add lead magnet tracking fields to offers table
Run this once to add new columns to existing database
"""
import sys
import os

# Add app directory to path
app_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, app_dir)

from sqlalchemy import text
from db.session import engine
import logging

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def migrate():
    """Add lead magnet tracking fields to offers table"""
    try:
        with engine.connect() as conn:
            # Check if columns already exist
            check_query = text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name='offers' AND column_name='lesson_clicked_at'
            """)
            result = conn.execute(check_query)
            if result.fetchone():
                logger.info("Migration already applied - columns exist")
                return
            
            # Add new columns
            logger.info("Adding lead magnet tracking columns to offers table...")
            
            conn.execute(text("""
                ALTER TABLE offers 
                ADD COLUMN lesson_clicked_at TIMESTAMP WITH TIME ZONE,
                ADD COLUMN first_reminder_sent TIMESTAMP WITH TIME ZONE,
                ADD COLUMN second_reminder_sent TIMESTAMP WITH TIME ZONE
            """))
            
            # Create index on lesson_clicked_at for faster queries
            conn.execute(text("""
                CREATE INDEX IF NOT EXISTS ix_offers_lesson_clicked_at 
                ON offers(lesson_clicked_at)
            """))
            
            conn.commit()
            logger.info("✅ Migration completed successfully!")
            
    except Exception as e:
        logger.error(f"❌ Migration failed: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    migrate()

