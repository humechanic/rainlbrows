from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
import env
import logging

logger = logging.getLogger(__name__)

# Create engine
engine = create_engine(
    env.DATABASE_URL,
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

