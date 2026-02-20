from app.services.calc import calculate_longest_streak, get_best_reading_time, get_daily_reading_stats
from datetime import datetime, timedelta

class MockLog:
    def __init__(self, start, end, created_at):
        self.start_page = start
        self.end_page = end
        self.created_at = created_at

def test_longest_streak():
    base = datetime.now()
    dates = [
        base - timedelta(days=0),
        base - timedelta(days=1),
        base - timedelta(days=3), # gap
        base - timedelta(days=4),
        base - timedelta(days=5),
        base - timedelta(days=6),
    ]
    # Streaks are: [0, 1] (len 2) and [3, 4, 5, 6] (len 4)
    assert calculate_longest_streak(dates) == 4
    print("✅ longest_streak test passed!")

def test_best_time():
    logs = [
        MockLog(1, 10, datetime(2024, 1, 1, 6, 0)), # Fajr
        MockLog(1, 10, datetime(2024, 1, 2, 6, 30)), # Fajr
        MockLog(1, 10, datetime(2024, 1, 3, 14, 0)), # After Dhuhr
    ]
    assert get_best_reading_time(logs) == "After Fajr"
    print("✅ best_time test passed!")

def test_daily_stats():
    now = datetime.now()
    logs = [
        MockLog(1, 10, now),
        MockLog(11, 25, now - timedelta(days=1)),
    ]
    stats = get_daily_reading_stats(logs, days=7)
    assert len(stats) == 7
    assert stats[-1]["pages"] == 10 # Today
    assert stats[-2]["pages"] == 15 # Yesterday
    print("✅ daily_stats test passed!")

if __name__ == "__main__":
    test_longest_streak()
    test_best_time()
    test_daily_stats()
