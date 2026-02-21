import asyncio
from app.database import AsyncSessionLocal
from sqlalchemy import text
async def main():
    async with AsyncSessionLocal() as db:
        res = await db.execute(text("SELECT 1"))
        print(res.scalar())
asyncio.run(main())
