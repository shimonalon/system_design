"""Database connection and session management"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from contextlib import contextmanager
from typing import Generator

from src.config import get_settings

# SQLAlchemy Base for all models
Base = declarative_base()


class Database:
    """Database connection manager"""
    
    def __init__(self, database_url: str):
        """
        Initialize database connection.
        
        Args:
            database_url: PostgreSQL connection string
        """
        self.engine = create_engine(database_url, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(bind=self.engine)
    
    def get_session(self) -> Session:
        """
        Get a new database session.
        
        Returns:
            Session: SQLAlchemy database session
        """
        return self.SessionLocal()
    
    @contextmanager
    def session_context(self) -> Generator[Session, None, None]:
        """
        Context manager for database sessions.
        
        Yields:
            Session: Database session
            
        Example:
            with db.session_context() as session:
                url = session.query(URL).filter_by(short_code='abc').first()
        """
        session = self.get_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
    
    def create_tables(self):
        """
        Create all tables in the database.
        
        This should be called once during application startup.
        """
        Base.metadata.create_all(self.engine)


# Global database instance
_db_instance = None

def get_db() -> Database:
    """
    Get the global database instance.
    
    Returns:
        Database: Configured database connection
    """
    global _db_instance
    if _db_instance is None:
        _db_instance = Database(get_settings().DATABASE_URL)
    return _db_instance
