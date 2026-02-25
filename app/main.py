from fastapi import FastAPI
from app.database import engine, Base
from app.models import user
from app.routes import user_routes

app = FastAPI(title="Blackjack Analytics API")

app.include_router(user_routes.router)

# Create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "Blackjack Analytics API is running"}