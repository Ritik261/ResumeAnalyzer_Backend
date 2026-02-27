from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=True)
sessionLocal = sessionmaker(autocommit = False, autoflush=False, bind = engine)
Base = declarative_base()

try:
    with engine.connect() as conn:
        print("DB Connected")
except:
    print("DB not connected")       

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()    