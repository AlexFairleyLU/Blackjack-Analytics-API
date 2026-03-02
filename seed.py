from app.database import SessionLocal, engine, Base
from app.models.user_model import User
from app.models.session_model import GameSession
from app.models.hand_model import Hand
from app.routes.user_routes import hash_password

import random

db = SessionLocal()

def seed():

    print("Seeding database...")

    # Optional: clear tables (safe for development only)
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # Create users
    user1 = User(username="alice", hashed_password=hash_password("password123"))
    user2 = User(username="bob", hashed_password=hash_password("password123"))

    db.add_all([user1, user2])
    db.commit()

    db.refresh(user1)
    db.refresh(user2)

    for user in [user1, user2]:
        for _ in range(3):  # 3 sessions each

            session = GameSession(user_id=user.id)
            db.add(session)
            db.commit()
            db.refresh(session)

            for _ in range(20):  # 20 hands per session

                bet = random.choice([10, 20, 50, 100])
                player_score = random.randint(15, 23)
                dealer_score = random.randint(15, 23)

                is_win = player_score <= 21 and (
                    dealer_score > 21 or player_score > dealer_score
                )

                is_blackjack = player_score == 21

                hand = Hand(
                    session_id=session.id,
                    bet_amount=bet,
                    player_score=player_score,
                    dealer_score=dealer_score,
                    is_win=is_win,
                    is_blackjack=is_blackjack
                )

                db.add(hand)

            db.commit()

    print("Seeding complete.")

if __name__ == "__main__":
    seed()