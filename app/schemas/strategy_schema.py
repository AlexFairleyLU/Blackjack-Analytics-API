from pydantic import BaseModel

class StrategyRecommendationResponse(BaseModel):
    player_total: int
    dealer_card: int
    hand_type: str
    recommended_action: str