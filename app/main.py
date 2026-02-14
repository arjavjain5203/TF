from fastapi import FastAPI
from app.routers import webhook
from app.utils.logging import setup_logging

logger = setup_logging()

app = FastAPI(title="Family Tree WhatsApp Bot")

app.include_router(webhook.router)

@app.get("/")
async def root():
    return {"message": "Family Tree Bot API is running"}
