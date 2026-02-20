import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

# Railway DB (preferred / internal)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+psycopg2://postgres:ioyyZhmTWeAuEJOedjKOntPekUSwILcH@postgres.railway.internal:5432/railway"
)

# Local (keep commented, don't remove)
# DATABASE_URL = "postgresql+psycopg2://postgres:009988@localhost:5432/Qurantracker"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
