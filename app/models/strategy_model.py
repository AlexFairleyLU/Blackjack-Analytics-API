from sqlalchemy import Column, Integer, String
from app.database import Base

class BasicStrategy(Base):
    __tablename__ = "basic_strategy"

    id = Column(Integer, primary_key=True, index=True)

    player_total = Column(Integer, nullable=False)
    dealer_card = Column(Integer, nullable=False)

    hand_type = Column(String, nullable=False)  
    # values: "hard", "soft", "pair"

    recommended_action = Column(String, nullable=False)
    # values: hit, stand, double, split