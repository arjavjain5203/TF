import asyncio
from app.database import AsyncSessionLocal
from app.services.chatbot_service import ChatbotService
from app.services.user_service import UserService
from app.services.member_service import MemberService
from app.services.tree_service import TreeService
from app.models.tree import Role
from datetime import date
from app.models.member import Gender

async def main():
    async with AsyncSessionLocal() as db:
        user_service = UserService(db)
        user = await user_service.get_or_create_user("whatsapp:+919310082225")
        
        # setup state to be EVENT_DATE as if we just chose it
        bot = ChatbotService(db)
        
        # Ensure user has a tree and member
        tree_service = TreeService(db)
        tree = await tree_service.create_tree(user)
        member_service = MemberService(db)
        member = await member_service.create_member(tree.id, "arjav", date(2000, 1, 1), Gender.MALE, 1)
        
        # update state
        await user_service.update_state(user.id, "EVENT_DATE", {"member_id": member.id, "event_type": "graduation year"})
        
        # Handle message
        res = await bot.handle_message("whatsapp:+919310082225", "01-01-2027")
        print("\n\nRESULT:")
        print(res)

asyncio.run(main())
