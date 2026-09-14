from database import get_connection
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()

connection = get_connection()
cursor = connection.cursor()

users = {
    1: "Peter123!",
    2: "Peter456!",
    3: "Shina123!",
    5: "Mum123!",
    6: "Dad123!"
}

try:
    for user_id, password in users.items():

        hashed_password = password_hash.hash(password)

        cursor.execute(
            """
            UPDATE users
            SET password_hash = %s
            WHERE id = %s
            """,
            (hashed_password, user_id)
        )

    connection.commit()

    print("Password hashes added successfully!")

except Exception:
    connection.rollback()
    raise

finally:
    cursor.close()
    connection.close()