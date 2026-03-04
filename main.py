from fastapi import FastAPI
from app.routes import router
from database.db import engine, Base
from app.middleware import APIKeyMiddleware

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.add_middleware(APIKeyMiddleware)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Secure API Key Manager Running"}