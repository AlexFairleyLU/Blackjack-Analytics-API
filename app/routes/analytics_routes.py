from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.hand_model import Hand
from app.models.session_model import GameSession
from app.models.user_model import User

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/session/{session_id}")
def session_analytics(session_id: int, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    total_hands = db.query(func.count(Hand.id)).filter(Hand.session_id == session_id).scalar()
    wins = db.query(func.count(Hand.id)).filter(
        Hand.session_id == session_id,
        Hand.is_win == True
    ).scalar()

    blackjacks = db.query(func.count(Hand.id)).filter(
        Hand.session_id == session_id,
        Hand.is_blackjack == True
    ).scalar()

    total_bet = db.query(func.sum(Hand.bet_amount)).filter(
        Hand.session_id == session_id
    ).scalar() or 0

    win_bet = db.query(func.sum(Hand.bet_amount)).filter(
        Hand.session_id == session_id,
        Hand.is_win == True
    ).scalar() or 0

    loss_bet = db.query(func.sum(Hand.bet_amount)).filter(
        Hand.session_id == session_id,
        Hand.is_win == False
    ).scalar() or 0

    win_rate = (wins / total_hands * 100) if total_hands else 0
    blackjack_rate = (blackjacks / total_hands * 100) if total_hands else 0
    profit = win_bet - loss_bet
    avg_bet = (total_bet / total_hands) if total_hands else 0

    return {
        "session_id": session_id,
        "total_hands": total_hands,
        "win_rate": round(win_rate, 2),
        "blackjack_rate": round(blackjack_rate, 2),
        "profit": round(profit, 2),
        "average_bet": round(avg_bet, 2)
    }

@router.get("/user/{user_id}")
def user_analytics(user_id: int, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    total_hands = db.query(func.count(Hand.id))\
        .join(GameSession)\
        .filter(GameSession.user_id == user_id)\
        .scalar()

    wins = db.query(func.count(Hand.id))\
        .join(GameSession)\
        .filter(GameSession.user_id == user_id, Hand.is_win == True)\
        .scalar()

    total_bet = db.query(func.sum(Hand.bet_amount))\
        .join(GameSession)\
        .filter(GameSession.user_id == user_id)\
        .scalar() or 0

    loss_bet = db.query(func.sum(Hand.bet_amount))\
        .join(GameSession)\
        .filter(GameSession.user_id == user_id, Hand.is_win == False)\
        .scalar() or 0

    win_bet = db.query(func.sum(Hand.bet_amount))\
        .join(GameSession)\
        .filter(GameSession.user_id == user_id, Hand.is_win == True)\
        .scalar() or 0

    win_rate = (wins / total_hands * 100) if total_hands else 0
    profit = win_bet - loss_bet

    return {
        "user_id": user_id,
        "total_hands": total_hands,
        "win_rate": round(win_rate, 2),
        "profit": round(profit, 2),
        "total_bet": round(total_bet, 2)
    }