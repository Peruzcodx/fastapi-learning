from database import get_connection

connection = get_connection()
cursor = connection.cursor()

try:
    cursor.execute("""
        ALTER TABLE public.users
        ALTER COLUMN email SET NOT NULL
    """)

    cursor.execute("""
        ALTER TABLE public.users
        ALTER COLUMN password_hash SET NOT NULL
    """)

    connection.commit()

    print("Authentication columns are now required!")

except Exception:
    connection.rollback()
    raise

finally:
    cursor.close()
    connection.close()