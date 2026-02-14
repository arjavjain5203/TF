import sys
import os

# Set dummy env vars for testing
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///./test.db"
os.environ["TWILIO_ACCOUNT_SID"] = "AC_TEST"
os.environ["TWILIO_AUTH_TOKEN"] = "AUTH_TEST"
os.environ["TWILIO_PHONE_NUMBER"] = "whatsapp:+14155238886"

from app.database import Base
from app.models.user import User
from app.models.tree import Tree, TreeAccess
from app.models.member import Member, Relationship

print(f"Tables in metadata: {Base.metadata.tables.keys()}")
