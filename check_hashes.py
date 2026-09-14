from database import get_connection

connection = get_connection()
cursor = connection.cursor()

cursor.execute("""
    SELECT id, email, password_hash
    FROM public.users
    WHERE id = 1
""")

row = cursor.fetchone()

if row:
    password_hash = row[2]

    print("Length:", len(password_hash))
    print("Starts correctly:", password_hash.startswith("$argon2id$"))
    print("Number of $ separators:", password_hash.count("$"))
    print("Parts:", len(password_hash.split("$")))

cursor.close()
connection.close()