from fastapi import APIRouter, Depends, Header, HTTPException
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

@router.get("/secure-data")
def protected_data(x_api_key: str = Header(None)):
    return {"message": "You accessed protected data"}

@router.post("/revoke-key")
def revoke_key(api_key: str, db: Session = Depends(get_db)):

    hashed_key = hash_api_key(api_key)

    key = db.query(APIKey).filter(APIKey.hashed_key == hashed_key).first()

    if not key:
        raise HTTPException(status_code=404, detail="API key not found")

    key.is_active = False
    db.commit()

    return {"message": "API key revoked successfully"}