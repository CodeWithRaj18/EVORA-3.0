⚡ EVORA 3.0
EV Charging Station Slot Booking Backend API

EVORA-3.0 is a FastAPI-based backend system for managing EV charging stations, slot bookings, wallet transactions, and emergency vehicle overrides.

Built during a hackathon, it focuses on:

Real-time slot booking

Booking lifecycle automation

Host & admin management

Wallet transactions

Emergency vehicle priority system

🚀 Tech Stack

Framework: FastAPI

Database: SQLite (lax_ev_stations.db)

ORM: SQLAlchemy

Scheduler: APScheduler

Authentication: JWT

Email Service: SMTP (OTP verification)



🧠 System Architecture
Client (Frontend / App)
        ↓
FastAPI Backend (main.py)
        ↓
Routers (Auth, Booking, Stations, Wallet, Admin)
        ↓
Booking Domain Logic
        ↓
SQLAlchemy ORM
        ↓
SQLite Database

📂 Project Structure
backend/
│
├── main.py                     # Application entry point
├── dependencies.py             # JWT, DB session, shared dependencies
│
├── database/
│   ├── database.py             # Engine & Session
│   ├── migrate_emergency.py
│   └── migrate_wallet_station.py
│
├── models/                     # ORM Models
│
├── booking_domain/
│   ├── booking_service.py
│   ├── booking_routes.py
│   └── lifecycle_scheduler.py
│
└── routes/                     # Other API routes
    ├── auth
    ├── stations
    ├── wallet
    ├── admin
    └── cars
🔄 Booking Lifecycle

A booking transitions automatically through states:

UPCOMING → ACTIVE → COMPLETED
         ↘
         CANCELLED

User books slot → UPCOMING

Scheduler checks time → ACTIVE

After slot ends → COMPLETED

User can cancel before activation

Handled by:

booking_service.py

lifecycle_scheduler.py

🗄️ Database Models

Core hierarchy:

User
 ├── Cars
 ├── WalletTransactions
 └── Bookings
        └── BookingSlots
                └── Slot
                        └── Charger
                                └── Station

Additional models:

Host

OTP

Message

Emergency fields

Wallet balance

⚙️ Startup Flow

When the app starts:

Creates all tables (Base.metadata.create_all)

Runs emergency migration

Runs wallet/station migration

Starts lifecycle scheduler

Mounts all routers

🔐 Authentication

JWT-based authentication

Access token expiry configurable

OTP email verification

Development console OTP bypass option

Environment variables required:

SECRET_KEY=
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=
SMTP_EMAIL=
SMTP_PASSWORD=
💰 Features
👤 User

Register & login

Add cars

Book EV slots

Cancel bookings

Wallet management

🏢 Host

Add charging stations

Add chargers

Manage slots

Track earnings

🛡️ Admin

Station approval

Platform analytics

Earnings overview

🚨 Emergency Vehicle Override

Emergency vehicles can override slot priority

Special flags in cars, bookings, and slots

🧪 Running Locally
1️⃣ Clone Repository
git clone https://github.com/CodeWithRaj18/EVORA-3.0.git
cd EVORA-3.0/backend
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run Server
uvicorn main:app --reload

Server runs at:

http://127.0.0.1:8000

Swagger docs:

http://127.0.0.1:8000/docs
📌 Development Notes

CORS is open (allow_origins=["*"]) — change before production.

SQLite used for hackathon simplicity.

Migrations run automatically at startup.

Designed modularly for PostgreSQL upgrade.

🧭 Future Improvements

PostgreSQL migration

Redis for real-time slot locking

Payment gateway integration

WebSocket live station status

Docker containerization

CI/CD pipeline
