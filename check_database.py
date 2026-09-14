from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("SELECT current_database()")
print("Database:", cursor.fetchone()[0])

cursor.execute("SELECT * FROM users")
rows = cursor.fetchall()

print("Users:", rows)

connection.close()