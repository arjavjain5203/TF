from fastapi import APIRouter, Request, Depends, Form, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.services.chatbot_service import ChatbotService
from app.config import get_settings
from twilio.request_validator import RequestValidator
import logging

router = APIRouter()
settings = get_settings()
logger = logging.getLogger(__name__)

async def validate_twilio_request(request: Request):
    validator = RequestValidator(settings.TWILIO_AUTH_TOKEN)
    form = await request.form()
    # Twilio sends data as form-encoded
    params = dict(form)
    url = str(request.url)
    
    # Render or proxies might change protocol to http, ensuring https matches Twilio's request
    if settings.ENVIRONMENT == "production":
         url = url.replace("http://", "https://")

    signature = request.headers.get("X-Twilio-Signature", "")
    
    if not validator.validate(url, params, signature):
        logger.warning(f"Invalid Twilio signature: {signature}")
        # In dev, might skip validation if needed, but safer to enforce or toggle
        if settings.ENVIRONMENT == "production":
             raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid signature")

@router.post("/webhook")
async def whatsapp_webhook(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    db: AsyncSession = Depends(get_db)
):
    # Validate signature
    # await validate_twilio_request(request) # Uncomment in production or properly configured dev

    chatbot = ChatbotService(db)
    response_str = await chatbot.handle_message(From, Body)
    
    from fastapi.responses import Response
    return Response(content=response_str, media_type="application/xml")
