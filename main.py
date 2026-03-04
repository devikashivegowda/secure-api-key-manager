from fastapi import FastAPI
from app.routes import router
from database.db import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Secure API Key Manager Running"}