import asyncio
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from app.models.user import User
from app.models.tree import Tree, TreeAccess, Role
from app.config import get_settings

async def setup_user():
    settings = get_settings()
    # Ensure URL is async compatible
    db_url = settings.DATABASE_URL.replace("postgres://", "postgresql+asyncpg://")
    if "sslmode=require" in db_url:
         db_url = db_url.replace("sslmode=require", "ssl=require") # asyncpg specific
    
    print(f"Connecting to database: {db_url}")
    
    engine = create_async_engine(db_url, echo=True)
    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    async with async_session() as session:
        phone = "+919310082225"
        stmt = select(User).filter(User.phone == phone)
        result = await session.execute(stmt)
        user = result.scalars().first()

        if not user:
            print(f"Creating user {phone}...")
            user = User(phone=phone)
            session.add(user)
            await session.commit()
            await session.refresh(user)
        else:
            print(f"User {phone} already exists.")

        # Check for tree
        stmt = select(Tree).filter(Tree.owner_id == user.id)
        result = await session.execute(stmt)
        tree = result.scalars().first()

        if not tree:
            print(f"Creating tree for user {phone}...")
            tree = Tree(owner_id=user.id)
            session.add(tree)
            
            # Grant OWNER access
            access = TreeAccess(tree=tree, user=user, role=Role.OWNER)
            session.add(access)
            
            await session.commit()
            print("Tree created successfully!")
        else:
            print(f"User already owns a tree (ID: {tree.id}).")

    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(setup_user())
