from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session import GameSession
from app.models.user import User
from app.schemas.session_schema import SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=SessionResponse)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_session = GameSession(user_id=session.user_id)

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session