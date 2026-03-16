from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session_model import GameSession
from app.models.user_model import User
from app.schemas.session_schema import SessionCreate, SessionResponse

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=SessionResponse, status_code=201)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    new_session = GameSession(user_id=session.user_id)

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

@router.get("/{session_id}")
def get_session(session_id: int, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session

@router.get("/user/{user_id}", summary="Get all sessions for a user")
def get_user_sessions(user_id: int, db: Session = Depends(get_db)):

    sessions = db.query(GameSession).filter(GameSession.user_id == user_id).all()
    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found for this user")

    return sessions

@router.delete("/{session_id}", status_code=204)
def delete_session(session_id: int, db: Session = Depends(get_db)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()

    return