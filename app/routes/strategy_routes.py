from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.strategy_model import BasicStrategy

router = APIRouter(prefix="/strategy", tags=["Strategy"])

@router.get("/recommendation", responses={404: {"description": "Strategy not found"}})
def get_strategy(
    player_total: int,
    dealer_card: int,
    hand_type: str,
    db: Session = Depends(get_db)
):

    strategy = db.query(BasicStrategy).filter(
        BasicStrategy.player_total == player_total,
        BasicStrategy.dealer_card == dealer_card,
        BasicStrategy.hand_type == hand_type
    ).first()

    if not strategy:
        raise HTTPException(
            status_code=404,
            detail="No strategy found for this hand"
        )

    return {
        "player_total": player_total,
        "dealer_card": dealer_card,
        "hand_type": hand_type,
        "recommended_action": strategy.recommended_action
    }