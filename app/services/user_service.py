from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from typing import Optional, Dict, Any

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_phone(self, phone: str) -> Optional[User]:
        result = await self.db.execute(select(User).filter(User.phone == phone))
        return result.scalars().first()

    async def create_user(self, phone: str, name: Optional[str] = None) -> User:
        user = User(phone=phone, name=name)
        self.db.add(user)
        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def update_state(self, user_id: int, state: str, data: Dict[str, Any] = None):
        result = await self.db.execute(select(User).filter(User.id == user_id))
        user = result.scalars().first()
        if user:
            user.current_state = state
            if data is not None:
                user.state_data = data
            await self.db.commit()
            await self.db.refresh(user)
        return user
    
    async def clear_state(self, user_id: int):
        await self.update_state(user_id, None, {})

    async def get_or_create_user(self, phone: str, name: Optional[str] = None) -> User:
        user = await self.get_user_by_phone(phone)
        if not user:
            user = await self.create_user(phone, name)
        return user
