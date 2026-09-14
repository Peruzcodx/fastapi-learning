from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id, user_id, product, amount
    FROM orders
    ORDER BY id
""")

rows = cursor.fetchall()

for row in rows:
    print(row)

connection.close()