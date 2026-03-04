from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from sqlalchemy.orm import Session
from database.db import SessionLocal
from app.models import APIKey
from app.services import hash_api_key

class APIKeyMiddleware(BaseHTTPMiddleware):

    async def dispatch(self, request: Request, call_next):

        # allow documentation routes without API key
        if request.url.path in ["/", "/docs", "/openapi.json", "/generate-key"]:
            response = await call_next(request)
            return response

        api_key = request.headers.get("x-api-key")

        if not api_key:
            raise HTTPException(status_code=401, detail="API key required")

        hashed_key = hash_api_key(api_key)

        db: Session = SessionLocal()

        key_exists = db.query(APIKey).filter(APIKey.hashed_key == hashed_key, ApiKey.is_active == True).first()

        db.close()

        if not key_exists:
            raise HTTPException(status_code=403, detail="Invalid API key")

        response = await call_next(request)

        return response