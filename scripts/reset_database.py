import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal, engine, Base
from app.models.user_model import User
from app.models.session_model import GameSession
from app.models.hand_model import Hand
from app.models.strategy_model import BasicStrategy

db = SessionLocal()

def seed():
    print("Dropping database...")
    Base.metadata.drop_all(bind=engine)

    print("Recreating database...")
    Base.metadata.create_all(bind=engine)

    print("Seeding complete.")

if __name__ == "__main__":
    seed()