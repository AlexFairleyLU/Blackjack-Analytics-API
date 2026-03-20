from fastapi import FastAPI
from app.database import engine, Base
from app.models import user_model
from app.models.strategy_model import BasicStrategy
from app.routes import user_routes, session_routes, hand_routes, analytics_routes, strategy_routes, auth_routes

app = FastAPI(
    title="Blackjack Analytics API",
    description="""
    A REST API for recording blackjack gameplay sessions and analysing player performance.

    Features include:
    - User and session management
    - Recording blackjack hands
    - Session statistics and analytics
    - Strategy recommendation based on Blackjack Basic Strategy
    - Evaluation of player decisions against optimal strategy
    """,
    version="1.0.0",
)

app.include_router(user_routes.router)
app.include_router(session_routes.router)
app.include_router(hand_routes.router)
app.include_router(analytics_routes.router)
app.include_router(strategy_routes.router)
app.include_router(auth_routes.router)

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {
        "api_name": "Blackjack Analytics API",
        "description": "REST API for recording blackjack sessions and analysing player decisions using blackjack basic strategy.",
        "documentation": "/docs",
        "key_features": [
            "User and session management",
            "Blackjack hand recording",
            "Session analytics",
            "Blackjack strategy recommendation",
            "Strategy accuracy analysis"
        ]
    }