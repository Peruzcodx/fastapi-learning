from fastapi import HTTPException
from schemas.user import User, UserCreate,UserUpdate
from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def get_user(user_id: int,connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )

        result = cursor.fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        return {
            "id": result[0],
            "name": result[1],
            "city": result[2]
        }
    
    finally:
        cursor.close()
def get_users(connection):
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM users")

        results = cursor.fetchall()


        return [
            {
                "id": row[0],
                "name": row[1],
                "city": row[2]
            }
            for row in results
        ]
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

def update_user(user_id: int, user: UserUpdate, connection ):
    cursor = connection.cursor()
    try:
        cursor.execute(
           """
            SELECT id, name, city
            FROM users 
            WHERE id = %s
           """,
            (user_id,)
        )

        result = cursor.fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        current_name = result[1]
        current_city = result[2]
        new_name = user.name if user.name is not None else current_name
        new_city = user.city if user.city is not None else current_city

        cursor.execute(
            """
            UPDATE users
            SET name = %s, city = %s
            WHERE id = %s
            RETURNING id, name, city
            """,
            (new_name, new_city, user_id)
        )

        updated = cursor.fetchone()

        connection.commit()

        return {
            "id": updated[0],
            "name": updated[1],
            "city": updated[2]
        }
    except Exception:
        connection.rollback()
        raise
    finally:
        cursor.close()

def delete_user(user_id: int, connection):
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT * FROM users WHERE id = %s",
            (user_id,)
        )

        result = cursor.fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        cursor.execute(
            "DELETE FROM users WHERE id = %s",
            (user_id,)
        )

        connection.commit()
      

        return {
            "message": "User deleted successfully",
            "id": user_id
        }
    except Exception:
        connection.rollback()
        raise 
    finally:
        cursor.close()

def get_user_by_email(email, connection):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, city, email, password_hash, role
            FROM public.users
            WHERE email = %s
            """,
            (email,)
        )

        return cursor.fetchone()

    finally:
        cursor.close()
def register_user(user, connection):
    existing_user = get_user_by_email(user.email, connection)

    if existing_user:
        raise ValueError("Email already registered")

    hashed_password = password_hash.hash(user.password)

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO public.users
            (name, city, email, password_hash, role)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id, name, city, email, role
            """,
            (
                user.name,
                user.city,
                user.email,
                hashed_password,
                "user"
            )
        )

        new_user = cursor.fetchone()

        connection.commit()

        return new_user

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()