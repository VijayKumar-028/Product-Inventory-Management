import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

db_url = os.getenv("DATABASE_URL")

engine = create_engine(db_url) # type: ignore

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
try:
    with engine.connect() as connection:
        print("Database connected successfully")
except Exception as e:
    print("Database connection failed:", e)