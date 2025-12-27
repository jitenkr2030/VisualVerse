"""
Shared Database Utilities for VisualVerse
Provides SQLAlchemy configuration and base model classes.
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import QueuePool

# Database configuration from environment
DATABASE_URL = os.getenv(
    "VISUALVERSE_DATABASE_URL",
    "postgresql://visualverse:visualverse@localhost:5432/visualverse"
)

# Create SQLAlchemy engine with connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    echo=False
)

# Create scoped session factory
db_session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine)
)

# Base class for all models
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
    """Initialize database by creating all tables."""
    from shared.database.models import (
        User, Role, Institution, Content, Concept,
        Lesson, Progress, Assessment, License, AuditLog
    )
    Base.metadata.create_all(bind=engine)


def get_db():
    """Get database session for dependency injection."""
    db = db_session()
    try:
        yield db
    finally:
        db.close()


def cleanup_db(exception=None):
    """Cleanup database session after request."""
    db = db_session()
    if exception:
        db.rollback()
    db.remove()
