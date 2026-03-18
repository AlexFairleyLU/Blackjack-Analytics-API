from pydantic import BaseModel

class SessionAnalyticsResponse(BaseModel):
    session_id: int
    total_hands: int
    win_rate: float
    blackjack_rate: float
    profit: float
    average_bet: float
    average_player_score: float

class UserAnalyticsResponse(BaseModel):
    user_id: int
    total_hands: int
    win_rate: float
    profit: float
    total_bet: float

class StrategyAccuracyResponse(BaseModel):
    session_id: int
    hands_evaluated: int
    correct_moves: int
    incorrect_moves: int
    strategy_accuracy: float