from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hand_model import Hand
from app.models.session_model import GameSession
from app.models.user_model import User
from app.schemas.hand_schema import HandCreate, HandResponse, HandUpdate
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/sessions/{session_id}/hands", tags=["Hands"])

@router.post("/", response_model=HandResponse, status_code=201,
            responses={404: {"description": "Session not found"}})
def create_hand(session_id: int, hand: HandCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    new_hand = Hand(
        session_id=session_id,
        player_action=hand.player_action,
        bet_amount=hand.bet_amount,
        player_score=hand.player_score,
        dealer_upcard=hand.dealer_upcard,
        dealer_score=hand.dealer_score,
        is_blackjack=hand.is_blackjack,
        is_win=hand.is_win
    )

    db.add(new_hand)
    db.commit()
    db.refresh(new_hand)

    return new_hand

@router.get("/", response_model=list[HandResponse],
            responses={404: {"description": "Session not found"}})
def get_hands(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    hands = db.query(Hand).filter(Hand.session_id == session_id).all()
    return hands

@router.put("/{hand_id}", response_model=HandResponse,
            responses={404: {"description": "Hand not found"}})
def update_hand(session_id: int, hand_id: int, hand_update: HandUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):

    hand = db.query(Hand).filter(
        Hand.id == hand_id,
        Hand.session_id == session_id
    ).first()

    if not hand:
        raise HTTPException(status_code=404, detail="Hand not found in this session")

    if hand.session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    update_data = hand_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(hand, key, value)

    db.commit()
    db.refresh(hand)

    return hand

@router.delete("/{hand_id}", status_code=204,
                responses={404: {"description": "Hand not found"}})
def delete_hand(session_id: int, hand_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    hand = db.query(Hand).filter(
        Hand.id == hand_id,
        Hand.session_id == session_id
    ).first()

    if not hand:
        raise HTTPException(status_code=404, detail="Hand not found in this session")

    if hand.session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    db.delete(hand)
    db.commit()

    return