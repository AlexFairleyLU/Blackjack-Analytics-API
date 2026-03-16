# Blackjack Analytics API

## Overview

This project implements a RESTful API for recording and analysing blackjack gameplay sessions.
The system allows users to store blackjack hands, track session statistics, and evaluate player decisions against optimal strategy.

The API supports:

* Recording blackjack sessions and individual hands
* Tracking betting outcomes and statistics
* Analysing player performance
* Comparing player decisions against **Blackjack Basic Strategy**

---

## Technologies Used

* **Python**
* **FastAPI** – REST API framework
* **PostgreSQL** – Relational database
* **SQLAlchemy** – ORM for database interaction
* **Uvicorn** – ASGI server
* **Swagger UI** – Automatic API documentation

---

## Project Structure

```
project_root
│
├── app
│   ├── models        # Database models
│   ├── routes        # API endpoints
│   ├── schemas       # Request/response schemas
│   └── database.py   # Database configuration
│
├── scripts
│   ├── reset_database.py   # Recreates database 
│   ├── seed_strategy.py   # Seeds blackjack strategy dataset
│   └── seed_test_data.py  # Seeds example users, sessions, and hands
│
├── main.py
├── requirements.txt
└── README.md
```

---

## Installation

### 1. Clone the repository

```
git clone https://github.com/AlexFairleyLU/Blackjack-Analytics-API
cd Blackjack-Analytics-API
```

### 2. Install dependencies

This project uses Python.

```
pip install -r requirements.txt
```

---

## Database Setup

This project uses PostgreSQL.

Create a database using PostgreSQL (e.g. blackjack_db).
The API reads the database connection string from the DATABASE_URL environment variable.

*The application reads its database configuration from the DATABASE_URL environment variable, allowing different environments (development, testing, production) to use different databases without modifying the source code.*

## Running the API

Start the development server:

```
uvicorn main:app --reload
```

The API will be available at:

```
http://127.0.0.1:8000
```

---

## API Documentation

Interactive documentation is automatically generated using Swagger.

Access it at:

```
http://127.0.0.1:8000/docs
```

From this interface you can:

* View all endpoints
* Test API requests
* Inspect request and response formats

---

## Seeding the Database

To populate the database with example data:

### Seed Blackjack Strategy Dataset

```
python scripts/seed_strategy.py
```

This will create:

* The complete basic strategy dataset

### Seed Example Users and Game Data

```
python scripts/seed_test_data.py
```

This will create:

* Example users
* Blackjack sessions
* Multiple hands per session
* Random player actions for analytics testing

---

## Example API Features

### Create a User

```
POST /users
```

### Start a Blackjack Session

```
POST /sessions
```

### Record a Hand

```
POST /sessions/{session_id}/hands
```

### Session Analytics

```
GET /analytics/session/{session_id}
```

Returns statistics such as:

* Win rate
* Total bets
* Blackjack frequency
* Profit/loss

### Strategy Accuracy

```
GET /analytics/session/{session_id}/strategy_accuracy
```

Evaluates how often the player followed optimal blackjack strategy.

---

## Strategy Dataset

The project includes a dataset representing **Blackjack Basic Strategy**, which provides optimal decisions for different player totals and dealer cards.

This dataset is used to:

* Recommend optimal actions
* Evaluate player decision accuracy

---

## Author

*Alexander Fairley* @ **University of Leeds**
