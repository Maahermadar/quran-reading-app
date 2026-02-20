import psycopg2

conn = psycopg2.connect(
    dbname='Qurantracker',
    user='postgres',
    password='009988',
    host='localhost',
    port='5432'
)
cur = conn.cursor()
cur.execute("ALTER TABLE users ADD COLUMN IF NOT EXISTS avatar_url VARCHAR;")
conn.commit()
print('Migration successful: avatar_url column added to users table.')
cur.close()
conn.close()
