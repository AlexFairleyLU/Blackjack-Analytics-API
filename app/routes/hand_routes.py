from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.hand import Hand
from app.models.session import GameSession
from app.schemas.hand_schema import HandCreate, HandResponse

router = APIRouter(prefix="/hands", tags=["Hands"])

@router.post("/", response_model=HandResponse)
def create_hand(hand: HandCreate, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == hand.session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    new_hand = Hand(**hand.dict())

    db.add(new_hand)
    db.commit()
    db.refresh(new_hand)

    return new_hand


@router.get("/session/{session_id}", response_model=list[HandResponse])
def get_hands_for_session(session_id: int, db: Session = Depends(get_db)):

    hands = db.query(Hand).filter(Hand.session_id == session_id).all()
    return hands