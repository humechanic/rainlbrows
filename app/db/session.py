from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.engine import Engine
import env
import logging
from typing import Optional

logger = logging.getLogger(__name__)

# Global engine and session factory (lazy initialization)
_engine: Optional[Engine] = None
_SessionLocal: Optional[sessionmaker] = None


def _get_database_url() -> str:
    """
    Get normalized database URL for psycopg3.
    SQLAlchemy 2.0+ requires explicit format postgresql+psycopg:// for psycopg3.
    """
    database_url = env.DATABASE_URL
    
    # Ensure we use postgresql+psycopg:// format for psycopg3
    # This explicitly tells SQLAlchemy to use psycopg3 (psycopg package)
    if database_url.startswith('postgresql://'):
        # Convert to explicit psycopg3 format
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        logger.info("Converted postgresql:// to postgresql+psycopg:// for explicit psycopg3 usage")
    elif database_url.startswith('postgresql+psycopg2://'):
        # Convert psycopg2 format to psycopg3
        database_url = database_url.replace('postgresql+psycopg2://', 'postgresql+psycopg://', 1)
        logger.info("Converted postgresql+psycopg2:// to postgresql+psycopg:// for psycopg3")
    # If already postgresql+psycopg://, keep it as is
    
    return database_url


def _initialize_engine():
    """Lazy initialization of database engine"""
    global _engine, _SessionLocal
    
    if _engine is not None:
        return
    
    try:
        database_url = _get_database_url()
        
        # Create engine with explicit psycopg3 driver
        # Format: postgresql+psycopg://user:password@host:port/database
        _engine = create_engine(
            database_url,
            pool_pre_ping=True,  # Verify connections before using
            echo=False  # Set to True for SQL query logging
        )
        
        # Create session factory
        _SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=_engine)
        
        logger.info("Database engine initialized successfully with psycopg3")
        
    except Exception as e:
        logger.error(f"Failed to initialize database engine: {e}", exc_info=True)
        # Don't raise - allow app to start without database
        # Functions will handle None engine gracefully
        _engine = None
        _SessionLocal = None


def get_engine() -> Optional[Engine]:
    """Get database engine (lazy initialization)"""
    if _engine is None:
        _initialize_engine()
    return _engine


# Backward compatibility: engine as module-level proxy
# This allows existing code to use `from db.session import engine`
class _EngineProxy:
    """Proxy for engine to support backward compatibility imports"""
    def connect(self, *args, **kwargs):
        """Connect to database"""
        engine = get_engine()
        if engine is None:
            raise RuntimeError("Database engine is not available. Database may not be initialized.")
        return engine.connect(*args, **kwargs)
    
    def __getattr__(self, name):
        """Delegate attribute access to actual engine"""
        engine = get_engine()
        if engine is None:
            raise RuntimeError("Database engine is not available. Database may not be initialized.")
        return getattr(engine, name)
    
    def __call__(self, *args, **kwargs):
        """Allow calling engine as function (if needed)"""
        engine = get_engine()
        if engine is None:
            raise RuntimeError("Database engine is not available. Database may not be initialized.")
        return engine(*args, **kwargs)

# Module-level engine for backward compatibility
# Usage: from db.session import engine
engine = _EngineProxy()


def get_db() -> Session:
    """Get database session (generator for dependency injection)"""
    if _SessionLocal is None:
        _initialize_engine()
    
    if _SessionLocal is None:
        raise RuntimeError("Database session factory is not available. Database may not be initialized.")
    
    db = _SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_db_session() -> Session:
    """Get database session (non-generator version for direct use)"""
    if _SessionLocal is None:
        _initialize_engine()
    
    if _SessionLocal is None:
        raise RuntimeError("Database session factory is not available. Database may not be initialized.")
    
    return _SessionLocal()

