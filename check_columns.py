from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT column_name
    FROM information_schema.columns
    WHERE table_schema = 'public'
      AND table_name = 'users'
    ORDER BY ordinal_position
""")

print("public.users columns:")

for row in cursor.fetchall():
    print(row[0])

cursor.close()
connection.close()