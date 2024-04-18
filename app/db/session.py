import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_CA_CERT = os.getenv("CA_CERT_PATH")
if DATABASE_CA_CERT is None:

    engine = create_engine("sqlite:///./sql_app.db", connect_args={"check_same_thread": False}, pool_size=15, max_overflow=20)
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    engine = create_engine(DATABASE_URL, connect_args={
        "ssl": {
            "ca": DATABASE_CA_CERT
        }
    })
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.commit()
        db.close()
