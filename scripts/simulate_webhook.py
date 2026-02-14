import asyncio
import sys
import os

# Ensure app is in path
sys.path.append(os.getcwd())

from app.services.chatbot_service import ChatbotService
from app.database import AsyncSessionLocal
from app.models.user import User
from sqlalchemy.future import select

async def simulate_chat():
    print("--- 🌳 Family Tree Bot Simulator 🌳 ---")
    print("Type your message and press Enter. Type 'quit' to exit.")
    
    phone_number = "+919310082225" # Use the number we set up
    print(f"Simulating user: {phone_number}")

    async with AsyncSessionLocal() as db:
        service = ChatbotService(db)
        
        # Ensure user exists for simulation context (though service handles get_or_create)
        # We just want to make sure the loop works.
        
        while True:
            user_input = input(f"You ({phone_number}): ")
            if user_input.lower() in ['quit', 'exit']:
                break
            
            try:
                # Mocking the call that webhook normally makes
                # The service returns a TwiML string.
                # structure: <Response><Message>...</Message></Response>
                response_xml = await service.handle_message(
                    from_number=f"whatsapp:{phone_number}",
                    body=user_input
                )
                
                # Simple parsing to extract the message body for display
                import xml.etree.ElementTree as ET
                try:
                    root = ET.fromstring(response_xml)
                    message_body = root.find("Message").text
                    print(f"Bot: {message_body}")
                except Exception:
                    print(f"Bot (Raw XML): {response_xml}")
                    
            except Exception as e:
                print(f"Error: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    try:
        asyncio.run(simulate_chat())
    except KeyboardInterrupt:
        print("\nExiting simulator.")
