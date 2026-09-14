from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id, name, email, role
    FROM public.users
    ORDER BY id
""")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()