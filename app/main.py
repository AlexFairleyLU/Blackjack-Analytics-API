from fastapi import FastAPI

app = FastAPI(title="Blackjack Analytics API")

@app.get("/")
def root():
    return {"message": "Blackjack Analytics API is running"}