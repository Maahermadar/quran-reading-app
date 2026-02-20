from datetime import datetime
import math

TOTAL_PAGES = 600

def calculate_pages_read(start: int, end: int) -> int:
    """
    Circular 1..600 logic.
    If end < start, it means user wrapped past 600.
    """
    if end >= start:
        return end - start + 1
    # Wrap-around
    return (TOTAL_PAGES - start + 1) + end

def completions_in_log(start: int, end: int) -> int:
    """
    Detects if a reading session completed a full Quran cycle.
    """
    if end < start:
        return 1
    if end == TOTAL_PAGES and start <= TOTAL_PAGES:
        return 1
    return 0

def get_juz_from_page(page: int) -> int:
    """
    30 Juz, 20 pages each.
    """
    if page <= 0: return 1
    if page > TOTAL_PAGES: return 30
    return ((page - 1) // 20) + 1

def calculate_progress_percentage(page: int) -> float:
    return round((page / TOTAL_PAGES) * 100, 1)

def calculate_streak(log_dates: list[datetime]) -> int:
    """
    Given a list of sorted unique dates (recent first), calculate current consecutive days.
    """
    if not log_dates:
        return 0
    
    # Sort dates descending (newest first)
    sorted_dates = sorted(list(set(d.date() for d in log_dates)), reverse=True)
    
    import datetime as dt
    today = dt.date.today()
    
    streak = 0
    current_check = today
    
    # If no log today, check if yesterday had a log (to keep streak alive)
    if sorted_dates[0] < today:
        if sorted_dates[0] == today - dt.timedelta(days=1):
            current_check = today - dt.timedelta(days=1)
        else:
            return 0
            
    for d in sorted_dates:
        if d == current_check:
            streak += 1
            current_check -= dt.timedelta(days=1)
        else:
            break
            
    return streak

def calculate_longest_streak(log_dates: list[datetime]) -> int:
    """
    Finds the maximum consecutive reading days in history.
    """
    if not log_dates:
        return 0
        
    sorted_dates = sorted(list(set(d.date() for d in log_dates)))
    if not sorted_dates:
        return 0
        
    import datetime as dt
    max_streak = 0
    current_streak = 0
    prev_date = None
    
    for d in sorted_dates:
        if prev_date is None or d == prev_date + dt.timedelta(days=1):
            current_streak += 1
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 1
        prev_date = d
        
    return max(max_streak, current_streak)

def get_best_reading_time(logs: list) -> str:
    """
    Analyzes log timestamps to find the most frequent reading hour category.
    """
    if not logs:
        return "N/A"
        
    hours = [log.created_at.hour for log in logs]
    if not hours:
        return "N/A"
        
    from collections import Counter
    most_common_hour = Counter(hours).most_common(1)[0][0]
    
    if 4 <= most_common_hour < 8:
        return "After Fajr"
    elif 8 <= most_common_hour < 12:
        return "Morning"
    elif 12 <= most_common_hour < 15:
        return "After Dhuhr"
    elif 15 <= most_common_hour < 18:
        return "After Asr"
    elif 18 <= most_common_hour < 21:
        return "After Maghrib"
    elif 21 <= most_common_hour or most_common_hour < 4:
        return "Night/Isha"
        
    return "Random"

def get_daily_reading_stats(logs: list, days: int = 7) -> list:
    """
    Aggregates pages read for each of the last 'days' days.
    Returns a list of dicts: [{"day": "Mon", "pages": 10}, ...]
    """
    import datetime as dt
    today = dt.date.today()
    stats = []
    
    # Identify last 7 days
    days_list = [(today - dt.timedelta(days=i)) for i in range(days)]
    days_list.reverse() # Oldest to newest (Mon -> Sun if today is Sun)
    
    for d in days_list:
        pages_today = 0
        for log in logs:
            if log.created_at.date() == d:
                pages_today += calculate_pages_read(log.start_page, log.end_page)
        
        stats.append({
            "day": d.strftime("%a"),
            "pages": pages_today,
            "is_today": d == today
        })
        
    return stats

def calculate_average_pages(logs: list, days: int = 7) -> float:
    """
    Calculates average pages read per day over the last 'days' days.
    """
    if not logs:
        return 0.0
        
    import datetime as dt
    cutoff = datetime.utcnow().date() - dt.timedelta(days=days-1)
    
    total_pages = 0
    # Use a set to count active days if we want avg over active days, 
    # but requirement said "per day over the last X days".
    for log in logs:
        if log.created_at.date() >= cutoff:
            total_pages += calculate_pages_read(log.start_page, log.end_page)
            
    return round(total_pages / days, 1)
