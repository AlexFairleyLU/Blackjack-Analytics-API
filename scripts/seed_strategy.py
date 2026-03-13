import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database import SessionLocal
from app.models.strategy_model import BasicStrategy

db = SessionLocal()

def seed():

    print("Seeding blackjack strategy dataset...")

    # clear existing data
    db.query(BasicStrategy).delete()


    def dealer_range():
        return range(2, 12)  # 11 = Ace


    def add_row(player_total, dealer_card, hand_type, action):
        row = BasicStrategy(
            player_total=player_total,
            dealer_card=dealer_card,
            hand_type=hand_type,
            recommended_action=action
        )
        db.add(row)


    # ----------------------------
    # HARD TOTAL STRATEGY
    # ----------------------------

    for dealer in dealer_range():
        for total in range(5, 9):
            add_row(total, dealer, "hard", "hit")

    for dealer in dealer_range():
        action = "double" if 3 <= dealer <= 6 else "hit"
        add_row(9, dealer, "hard", action)

    for dealer in dealer_range():
        action = "double" if dealer <= 9 else "hit"
        add_row(10, dealer, "hard", action)

    for dealer in dealer_range():
        add_row(11, dealer, "hard", "double")

    for dealer in dealer_range():
        action = "stand" if 4 <= dealer <= 6 else "hit"
        add_row(12, dealer, "hard", action)

    for total in range(13, 17):
        for dealer in dealer_range():
            action = "stand" if dealer <= 6 else "hit"
            add_row(total, dealer, "hard", action)

    for dealer in dealer_range():
        add_row(17, dealer, "hard", "stand")

    for dealer in dealer_range():
        add_row(18, dealer, "hard", "stand")

    for dealer in dealer_range():
        add_row(19, dealer, "hard", "stand")

    for dealer in dealer_range():
        add_row(20, dealer, "hard", "stand")


    # ----------------------------
    # SOFT TOTAL STRATEGY
    # ----------------------------

    for total in [13, 14]:
        for dealer in dealer_range():
            action = "double" if 5 <= dealer <= 6 else "hit"
            add_row(total, dealer, "soft", action)

    for total in [15, 16]:
        for dealer in dealer_range():
            action = "double" if 4 <= dealer <= 6 else "hit"
            add_row(total, dealer, "soft", action)

    for dealer in dealer_range():
        action = "double" if 3 <= dealer <= 6 else "hit"
        add_row(17, dealer, "soft", action)

    for dealer in dealer_range():
        if 3 <= dealer <= 6:
            action = "double"
        elif dealer in [2, 7, 8]:
            action = "stand"
        else:
            action = "hit"
        add_row(18, dealer, "soft", action)

    for dealer in dealer_range():
        add_row(19, dealer, "soft", "stand")

    for dealer in dealer_range():
        add_row(20, dealer, "soft", "stand")


    # ----------------------------
    # PAIR STRATEGY
    # ----------------------------

    for dealer in dealer_range():
        add_row(12, dealer, "pair", "split")  # AA

    for dealer in dealer_range():
        add_row(20, dealer, "pair", "stand")  # TT

    for dealer in dealer_range():
        add_row(16, dealer, "pair", "split")  # 88

    for dealer in dealer_range():
        action = "split" if dealer in [2,3,4,5,6,8,9] else "stand"
        add_row(18, dealer, "pair", action)  # 99

    db.commit()

    print("Seeding complete.")

if __name__ == "__main__":
    seed()