from database import get_connection


connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        city TEXT NOT NULL
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS orders (
        id SERIAL PRIMARY KEY,
        user_id INTEGER REFERENCES users(id),
        product TEXT NOT NULL,
        amount NUMERIC NOT NULL
    )
""")

connection.commit()

print("Database tables created successfully!")

cursor.close()
connection.close()