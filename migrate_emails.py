from database import get_connection

connection = get_connection()
cursor = connection.cursor()

users = {
    1: "peter1@example.com",
    2: "peter2@example.com",
    3: "shina@example.com",
    5: "mum@example.com",
    6: "dad@example.com"
}

try:
    for user_id, email in users.items():
        cursor.execute(
            """
            UPDATE public.users
            SET email = %s
            WHERE id = %s
            """,
            (email, user_id)
        )

    connection.commit()

    print("Test emails added successfully!")

except Exception:
    connection.rollback()
    raise

finally:
    cursor.close()
    connection.close()
    