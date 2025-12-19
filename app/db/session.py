from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import env
import logging

logger = logging.getLogger(__name__)

# Normalize DATABASE_URL to use postgresql:// format
# SQLAlchemy 2.0+ will auto-detect psycopg3 (psycopg) if available
# The postgresql:// format allows SQLAlchemy to choose the best available driver
database_url = env.DATABASE_URL

# Convert postgresql+psycopg:// to postgresql:// for auto-detection
# SQLAlchemy 2.0+ prefers postgresql:// and will use psycopg3 if available
if database_url.startswith('postgresql+psycopg://'):
    # Replace with postgresql:// - SQLAlchemy will auto-detect psycopg3
    database_url = database_url.replace('postgresql+psycopg://', 'postgresql://', 1)
    logger.info("Converted postgresql+psycopg:// to postgresql:// for auto-detection")
elif database_url.startswith('postgresql+psycopg2://'):
    # Replace with postgresql:// - SQLAlchemy will use psycopg3 if available
    database_url = database_url.replace('postgresql+psycopg2://', 'postgresql://', 1)
    logger.info("Converted postgresql+psycopg2:// to postgresql:// for auto-detection")

# Create engine
# SQLAlchemy 2.0+ will automatically use psycopg3 (psycopg) if it's installed
# and fall back to psycopg2 if psycopg3 is not available
engine = create_engine(
    database_url,
    pool_pre_ping=True,  # Verify connections before using
    echo=False  # Set to True for SQL query logging
)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Session:
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session() -> Session:
    """Get database session (non-generator version for direct use)"""
    return SessionLocal()

