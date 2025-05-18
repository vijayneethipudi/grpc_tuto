from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from packages.models.user import Base

engine = create_engine("sqlite:///users.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create tables
Base.metadata.create_all(bind=engine)
