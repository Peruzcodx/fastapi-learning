from database import get_connection

connection = get_connection()
cursor = connection.cursor()

try:
    # First order — valid
    cursor.execute(
        """
        INSERT INTO orders (user_id, product, amount)
        VALUES (%s, %s, %s)
        """,
        (1, "Keyboard", 25000)
    )

    print("First order inserted.")

    # Second order — intentionally invalid
    cursor.execute(
        """
        INSERT INTO orders (user_id, product, amount)
        VALUES (%s, %s, %s)
        """,
        (999, "Monitor", 150000)
    )

    print("Second order inserted.")

    connection.commit()

except Exception as e:
    print("Error:", e)
    connection.rollback()
    print("Transaction rolled back.")

finally:
    connection.close()