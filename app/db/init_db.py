from db.base import Base
from db.session import get_engine
import logging

logger = logging.getLogger(__name__)


def init_db():
    """Initialize database - create all tables"""
    try:
        engine = get_engine()
        if engine is None:
            raise RuntimeError("Database engine is not available. Cannot initialize database.")
        
        # Import all models to ensure they are registered with Base
        from db.models import User, Offer
        
        # Create all tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error initializing database: {e}", exc_info=True)
        raise

