from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.services import generate_api_key, hash_api_key
from app.models import APIKey
from database.db import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/generate-key")
def create_key(db: Session = Depends(get_db)):
    api_key = generate_api_key()
    hashed_key = hash_api_key(api_key)

    new_key = APIKey(hashed_key=hashed_key)
    db.add(new_key)
    db.commit()

    return {
        "api_key": api_key
    }