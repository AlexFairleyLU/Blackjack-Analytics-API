from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.session_model import GameSession
from app.models.user_model import User
from app.schemas.session_schema import SessionResponse
from app.utils.dependencies import get_current_user

router = APIRouter(prefix="/sessions", tags=["Sessions"])

@router.post("/", response_model=SessionResponse, status_code=201,
            responses={404: {"description": "User not found"}})
def create_session(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    user = db.query(User).filter(User.id == current_user.id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    new_session = GameSession(user_id=current_user.id)

    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    return new_session

@router.get("/{session_id}", responses={404: {"description": "Session not found"}})
def get_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return session

@router.get("/user/{user_id}", summary="Get all sessions for a user",
            responses={404: {"description": "Sessions not found"}})
def get_user_sessions(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    sessions = db.query(GameSession).filter(GameSession.user_id == user_id).all()

    if user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")

    if not sessions:
        raise HTTPException(status_code=404, detail="No sessions found for this user")

    return sessions

@router.delete("/{session_id}", status_code=204,
                responses={404: {"description": "Session not found"}})
def delete_session(session_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    session = db.query(GameSession).filter(GameSession.id == session_id).first()

    if session.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorised")
    
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    db.delete(session)
    db.commit()

    return