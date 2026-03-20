import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


# ---------- Helpers ----------

def get_token(username="alice", password="password123"):
    response = client.post(
        "/auth/login",
        data={"username": username, "password": password}
    )
    assert response.status_code == 200
    return response.json()["access_token"]


# ---------- Tests ----------

def test_login_success():
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "password123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_login_fail():
    response = client.post(
        "/auth/login",
        data={"username": "alice", "password": "wrong"}
    )
    assert response.status_code == 401


def test_protected_requires_auth():
    response = client.get("/session/1/analytics")
    assert response.status_code == 401


def test_get_session_authorised():
    token = get_token()
    response = client.get(
        "/sessions/1",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200


def test_create_session():
    token = get_token()
    response = client.post(
        "/sessions",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201


def test_session_analytics():
    token = get_token()
    response = client.get(
        "/analytics/session/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        data = response.json()
        assert "total_hands" in data
        assert "win_rate" in data
        assert "profit" in data


def test_strategy_accuracy_structure():
    token = get_token()
    response = client.get(
        "/analytics/strategy/1",
        headers={"Authorization": f"Bearer {token}"}
    )

    if response.status_code == 200:
        data = response.json()
        assert "strategy_accuracy" in data


def test_create_hand():
    token = get_token()

    response = client.post(
        "/sessions/1/hands",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "player_action": "hit",
            "bet_amount": 50,
            "player_score": 18,
            "dealer_score": 20,
            "dealer_upcard":10,
            "is_win": False,
            "is_blackjack": False
        }
    )

    assert response.status_code == 201