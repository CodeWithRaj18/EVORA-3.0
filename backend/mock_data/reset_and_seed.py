"""Hackathon reset: delete SQLite DB and seed a clean coherent dataset.

Run:
  python -m mock_data.reset_and_seed

This will:
- delete backend/lax_ev_stations.db
- create tables
- seed: 1 admin(host), 2 users, 2 stations, chargers, and 3 days of 10-min slots

"""

import os
from datetime import datetime

from database.database import DB_PATH, engine, SessionLocal
from models import base  # noqa: F401
import models  # noqa: F401

from models.host import Host
from models.user import User
from models.station import Station
from models.charger import Charger


def reset_db_file():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"✅ Deleted DB: {DB_PATH}")


def seed():
    db = SessionLocal()

    # Admin (Host)
    admin = Host(
        id="admin-host-1",
        name="Admin",
        email="admin@evora.dev",
        password_hash="admin",
        is_verified=True,
    )
    db.add(admin)

    # Users (for booking layer later)
    u1 = User(
        id="user-1",
        name="Demo User",
        email="user1@evora.dev",
        password_hash="user",
        is_verified=True,
        is_profile_complete=True,
    )
    u2 = User(
        id="user-2",
        name="Second User",
        email="user2@evora.dev",
        password_hash="user",
        is_verified=True,
        is_profile_complete=True,
    )
    db.add_all([u1, u2])

    # Stations
    s1 = Station(
        id="station-1",
        host_id=admin.id,
        name="Downtown EV Hub",
        address="City Center",
        latitude="17.385044",
        longitude="78.486671",
        is_active=True,
    )
    s2 = Station(
        id="station-2",
        host_id=admin.id,
        name="Mall Parking Station",
        address="Central Mall",
        latitude="17.450000",
        longitude="78.500000",
        is_active=True,
    )
    db.add_all([s1, s2])
    db.commit()

    # Chargers (charger_type must be consistent everywhere)
    c1 = Charger(
        id="charger-1",
        station_id=s1.id,
        name="Charger A",
        charger_type="CCS2",
        power_kw="60",
        power_output_kw=60.0,
        default_price_30min=90.0,
        is_active=True,
        created_at=datetime.utcnow(),
    )
    c2 = Charger(
        id="charger-2",
        station_id=s1.id,
        name="Charger B",
        charger_type="Type2",
        power_kw="22",
        power_output_kw=22.0,
        default_price_30min=45.0,
        is_active=True,
        created_at=datetime.utcnow(),
    )
    c3 = Charger(
        id="charger-3",
        station_id=s2.id,
        name="Charger C",
        charger_type="CCS2",
        power_kw="120",
        power_output_kw=120.0,
        default_price_30min=120.0,
        is_active=True,
        created_at=datetime.utcnow(),
    )

    db.add_all([c1, c2, c3])
    db.commit()

    # Generate 3 days slots for each charger using the same function as API (import route handler)
    from routes.slots import generate_3days
    from schema.slot_engine import SlotGenerateRequest

    payload = SlotGenerateRequest(open_time="06:00", close_time="22:00")

    for cid in [c1.id, c2.id, c3.id]:
        generate_3days(charger_id=cid, payload=payload, db=db)

    db.close()
    print("✅ Seed complete")


def main():
    reset_db_file()
    base.Base.metadata.create_all(bind=engine)
    seed()


if __name__ == "__main__":
    main()
