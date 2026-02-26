from pydantic import BaseModel

class HandCreate(BaseModel):
    bet_amount: float
    player_score: int
    dealer_score: int
    is_blackjack: bool
    is_win: bool

class HandUpdate(BaseModel):
    bet_amount: float | None = None
    player_score: int | None = None
    dealer_score: int | None = None
    is_blackjack: bool | None = None
    is_win: bool | None = None

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