from sqlalchemy import Column, Integer, ForeignKey, Boolean, Float
from sqlalchemy.orm import relationship
from app.database import Base

class Hand(Base):
    __tablename__ = "hands"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("game_sessions.id"), nullable=False)

    bet_amount = Column(Float, nullable=False)
    player_score = Column(Integer, nullable=False)
    dealer_score = Column(Integer, nullable=False)

    is_blackjack = Column(Boolean, default=False)
    is_win = Column(Boolean, nullable=False)

    session = relationship("GameSession", backref="hands")