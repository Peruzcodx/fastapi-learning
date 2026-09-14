from database import get_connection
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

connection = get_connection()
cursor = connection.cursor()

cursor.execute(
    """
    SELECT email, password_hash
    FROM public.users
    WHERE email = %s
    """,
    ("peter1@example.com",)
)

user = cursor.fetchone()

if user is None:
    print("User not found")
else:
    email = user[0]
    stored_hash = user[1]

    print("User found:", email)

    password = "Peter123!"

    if password_hash.verify(password, stored_hash):
        print("Password is correct")
    else:
        print("Password is incorrect")

cursor.close()
connection.close()