"""
Quick integration test for the completion logic state machine.
Verifies: completion counted only once, cycle resets on next normal log.
"""
from app.db import database, models, schemas
from app.routers import logs, progress

class MockUser:
    def __init__(self, id):
        self.id = id

ERRORS = []

def check(label, actual, expected):
    if actual != expected:
        ERRORS.append(f"FAIL [{label}]: expected {expected}, got {actual}")
        print(f"  ❌ {label}: expected {expected}, got {actual}")
    else:
        print(f"  ✅ {label}: {actual}")

def test():
    db = next(database.get_db())
    import uuid
    unique_email = f"test_{uuid.uuid4()}@example.com"
    user = models.User(name="Test", email=unique_email, password_hash="x")
    db.add(user)
    db.commit()
    db.refresh(user)

    current_user = user

    print("\n--- Scenario 1: Normal reading (1→100) ---")
    logs.create_reading_log(schemas.ReadingLogCreate(start_page=1, end_page=100), db, current_user)
    prog = progress.get_progress(db, current_user)
    check("completions", prog["lifetime_completions"], 0)
    check("is_cycle_completed", prog["is_cycle_completed"], False)

    print("\n--- Scenario 2: Completion log (580→600) ---")
    logs.create_reading_log(schemas.ReadingLogCreate(start_page=580, end_page=600), db, current_user)
    prog = progress.get_progress(db, current_user)
    check("completions", prog["lifetime_completions"], 1)
    check("is_cycle_completed", prog["is_cycle_completed"], True)

    print("\n--- Scenario 3: Verify completion_counted on the log ---")
    last_log = db.query(models.ReadingLog).filter(
        models.ReadingLog.user_id == current_user.id
    ).order_by(models.ReadingLog.created_at.desc()).first()
    check("completion_counted on log", last_log.completion_counted, 1)

    print("\n--- Scenario 4: First new cycle log (1→2), success message should clear ---")
    logs.create_reading_log(schemas.ReadingLogCreate(start_page=1, end_page=2), db, current_user)
    prog = progress.get_progress(db, current_user)
    check("completions (unchanged)", prog["lifetime_completions"], 1)
    check("is_cycle_completed (reset)", prog["is_cycle_completed"], False)

    print("\n--- Scenario 5: Wrap-around completion (590→5) ---")
    logs.create_reading_log(schemas.ReadingLogCreate(start_page=590, end_page=5), db, current_user)
    prog = progress.get_progress(db, current_user)
    check("completions", prog["lifetime_completions"], 2)
    check("is_cycle_completed", prog["is_cycle_completed"], True)

    # Cleanup
    db.query(models.ReadingLog).filter(models.ReadingLog.user_id == current_user.id).delete()
    db.query(models.LifetimeStat).filter(models.LifetimeStat.user_id == current_user.id).delete()
    db.query(models.User).filter(models.User.id == current_user.id).delete()
    db.commit()

    if ERRORS:
        print(f"\n❌ {len(ERRORS)} test(s) failed.")
        for e in ERRORS:
            print(" ", e)
    else:
        print("\n✅ All scenarios passed!")

if __name__ == "__main__":
    test()
