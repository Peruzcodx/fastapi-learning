from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT constraint_name, constraint_type
    FROM information_schema.table_constraints
    WHERE table_schema = 'public'
      AND table_name = 'users'
      AND constraint_type = 'UNIQUE'
""")

print("Unique constraints:")

for row in cursor.fetchall():
    print(row)

cursor.close()
connection.close()