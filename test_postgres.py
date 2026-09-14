import psycopg

connection = psycopg.connect(
    host="localhost",
    port=5432,
    dbname="fastapi_learning",
    user="postgres",
    password="Yeyepeter123$"
)

print("Connected to PostgreSQL!")

connection.close()