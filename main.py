from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Secure API Key Manager Running"}