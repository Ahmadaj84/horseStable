from app import app, db
from models import Horse, Rider, Session

with app.app_context():
    db.create_all()

    # Only insert sample data if tables are empty
    if not Horse.query.first():
        db.session.add_all([
            Horse(name="Thunder", age=5),
            Horse(name="Storm", age=7)
        ])
        db.session.add_all([
            Rider(name="Alice", level="Intermediate"),
            Rider(name="Bob", level="Beginner")
        ])
        db.session.add_all([
            Session(date="2025-08-10", horse_id=1, rider_id=1),
            Session(date="2025-08-11", horse_id=2, rider_id=2)
        ])
        db.session.commit()
        print("✅ Database initialized with sample data.")
    else:
        print("ℹ Database already has data.")
