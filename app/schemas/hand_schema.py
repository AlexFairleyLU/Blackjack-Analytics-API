from pydantic import BaseModel

class HandCreate(BaseModel):
    session_id: int
    bet_amount: float
    player_score: int
    dealer_score: int
    is_blackjack: bool
    is_win: bool

class HandResponse(BaseModel):
    id: int
    session_id: int
    bet_amount: float
    player_score: int
    dealer_score: int
    is_blackjack: bool
    is_win: bool

    class Config:
        from_attributes = True