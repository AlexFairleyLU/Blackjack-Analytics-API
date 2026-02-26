from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hand import Hand
from app.models.session import GameSession
from app.schemas.hand_schema import HandCreate, HandResponse, HandUpdate

router = APIRouter(prefix="/sessions/{session_id}/hands", tags=["Hands"])

@router.post("/", response_model=HandResponse)
def create_hand(session_id: int, hand: HandCreate, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    new_hand = Hand(
        session_id=session_id,
        bet_amount=hand.bet_amount,
        player_score=hand.player_score,
        dealer_score=hand.dealer_score,
        is_blackjack=hand.is_blackjack,
        is_win=hand.is_win
    )

    db.add(new_hand)
    db.commit()
    db.refresh(new_hand)

    return new_hand


@router.get("/", response_model=list[HandResponse])
def get_hands(session_id: int, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    hands = db.query(Hand).filter(Hand.session_id == session_id).all()
    return hands

@router.put("/{hand_id}", response_model=HandResponse)
def update_hand(session_id: int, hand_id: int, hand_update: HandUpdate, db: Session = Depends(get_db)):

    hand = db.query(Hand).filter(
        Hand.id == hand_id,
        Hand.session_id == session_id
    ).first()

    if not hand:
        raise HTTPException(status_code=404, detail="Hand not found in this session")

    update_data = hand_update.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(hand, key, value)

    db.commit()
    db.refresh(hand)

    return hand

@router.delete("/{hand_id}", status_code=204)
def delete_hand(session_id: int, hand_id: int, db: Session = Depends(get_db)):

    hand = db.query(Hand).filter(
        Hand.id == hand_id,
        Hand.session_id == session_id
    ).first()

    if not hand:
        raise HTTPException(status_code=404, detail="Hand not found in this session")

    db.delete(hand)
    db.commit()

    return