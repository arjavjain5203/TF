import asyncio
import os
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"

from app.database import engine, Base, AsyncSessionLocal
from app.services.chatbot_service import ChatbotService
from app.services.user_service import UserService

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        bot = ChatbotService(db)
        phone = "whatsapp:+910000000000"
        
        async def send(msg):
            print(f"> {msg}")
            res = await bot.handle_message(phone, msg)
            if "Tree" in str(res) or "Gen" in str(res):
                print(str(res))
        
        await send("reset")
        await send("Hi")
        await send("2") # Manage tree
        await send("2") # Add member
        await send("Husband")
        await send("01-01-1980")
        await send("Male")
        await send("skip")
        
        await send("2") # Add member
        await send("Wife")
        await send("01-01-1985")
        await send("Female")
        await send("skip")
        await send("1") # Rel: Husband
        await send("4") # Spouse

        await send("2") # Add member
        await send("Son")
        await send("01-01-2010")
        await send("Male")
        await send("skip")
        await send("1") # Rel: Husband
        await send("3") # Child
        
        await send("2") # Add member
        await send("Brother")
        await send("01-01-1982")
        await send("Male")
        await send("skip")
        await send("1") # Rel: Husband
        await send("5") # Brother
        
        print("\n\n--- VIEW TREE ---")
        await send("1") # View tree

asyncio.run(main())
