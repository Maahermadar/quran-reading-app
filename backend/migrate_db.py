import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:009988@localhost:5432/Qurantracker")

def migrate():
    try:
        url = DATABASE_URL.replace("postgresql+psycopg2://", "postgresql://")
        conn = psycopg2.connect(url)
        cur = conn.cursor()

        print("Adding completion_counted column to reading_logs...")
        cur.execute("ALTER TABLE reading_logs ADD COLUMN IF NOT EXISTS completion_counted INTEGER DEFAULT 0;")

        print("Ensuring is_cycle_completed exists on lifetime_stats...")
        cur.execute("ALTER TABLE lifetime_stats ADD COLUMN IF NOT EXISTS is_cycle_completed INTEGER DEFAULT 0;")

        print("Ensuring avatar_url exists on users...")
        cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR;")

        conn.commit()
        cur.close()
        conn.close()
        print("✅ Migration successful!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")

if __name__ == "__main__":
    migrate()
