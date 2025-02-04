from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URL = "postgresql://library_db_user:billion@0.0.0.0:5432/library_db"
# DATABASE_URL = "sqlite:///library_system.db"

db_engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=db_engine)
Base = declarative_base()
print(f"Creating BASEEEEEE")

def get_db_session():
    session = SessionLocal()

    try:
        yield session
    finally:
        session.close()


def get_db_session_instance():
    session = SessionLocal()
    return session