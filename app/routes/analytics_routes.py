from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from app.database import get_db
from app.models.hand_model import Hand
from app.models.session_model import GameSession
from app.models.user_model import User
from app.models.strategy_model import BasicStrategy
from app.schemas.analytics_schema import SessionAnalyticsResponse, UserAnalyticsResponse, StrategyAccuracyResponse

router = APIRouter(tags=["Analytics"])

@router.get("/session/{session_id}/analytics", response_model=SessionAnalyticsResponse,
            responses={404: {"description": "Session not found"}})
def session_analytics(session_id: int, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    stats = db.query(
        func.count(Hand.id).label("total_hands"),
        func.sum(Hand.bet_amount).label("total_bet"),
        func.sum(
            case((Hand.is_win == True, Hand.bet_amount), else_=0)
        ).label("win_bet"),
        func.sum(
            case((Hand.is_win == False, Hand.bet_amount), else_=0)
        ).label("loss_bet"),
        func.sum(
            case((Hand.is_blackjack == True, 1), else_=0)
        ).label("blackjacks"),
        func.sum(
            case((Hand.is_win == True, 1), else_=0)
        ).label("wins")
    ).filter(Hand.session_id == session_id).one()

    avg_player_score = db.query(func.avg(Hand.player_score))\
    .filter(Hand.session_id == session_id)\
    .scalar() or 0

    win_rate = (stats.wins / stats.total_hands * 100) if stats.total_hands else 0
    blackjack_rate = (stats.blackjacks / stats.total_hands * 100) if stats.total_hands else 0
    profit = stats.win_bet - stats.loss_bet
    avg_bet = (stats.total_bet / stats.total_hands) if stats.total_hands else 0

    return {
        "session_id": session_id,
        "total_hands": stats.total_hands,
        "win_rate": round(win_rate, 2),
        "blackjack_rate": round(blackjack_rate, 2),
        "profit": round(profit, 2),
        "average_bet": round(avg_bet, 2),
        "average_player_score": round(avg_player_score, 2)
    }

@router.get("/user/{user_id}/analytics", response_model=UserAnalyticsResponse,
            responses={404: {"description": "User not found"}})
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

@router.get("/session/{session_id}/strategy_accuracy", response_model=StrategyAccuracyResponse,
            responses={404: {"description": "Session not found"}})
def session_strategy_accuracy(session_id: int, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    hands = db.query(Hand).filter(Hand.session_id == session_id).all()

    if not hands:
        return {
            "session_id": session_id,
            "hands_evaluated": 0,
            "correct_moves": 0,
            "incorrect_moves": 0,
            "strategy_accuracy": 0
        }

    correct = 0
    incorrect = 0

    for hand in hands:

        if not hand.player_action:
            continue

        strategy = db.query(BasicStrategy).filter(
            BasicStrategy.player_total == hand.player_score,
            BasicStrategy.dealer_card == hand.dealer_upcard,
            BasicStrategy.hand_type == "hard"
        ).first()

        if not strategy:
            continue

        if hand.player_action == strategy.recommended_action:
            correct += 1
        else:
            incorrect += 1

    total = correct + incorrect

    accuracy = (correct / total * 100) if total else 0

    return {
        "session_id": session_id,
        "hands_evaluated": total,
        "correct_moves": correct,
        "incorrect_moves": incorrect,
        "strategy_accuracy": round(accuracy, 2)
    }