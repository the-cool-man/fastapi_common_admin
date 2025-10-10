from db_connection.session import engine

try:
    with engine.connect() as conn:
        print("✅ PostgreSQL Connected Successfully!")
except Exception as e:
    print("❌ Connection Failed:", e)
