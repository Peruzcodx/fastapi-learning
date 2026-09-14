from fastapi import HTTPException

def create_order(order, current_user, connection):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            INSERT INTO orders (user_id, product, amount)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (current_user, order.product, order.amount)
        )

        order_id = cursor.fetchone()[0]

        connection.commit()

        return {
            "id": order_id,
            "user_id": current_user,
            "product": order.product,
            "amount": order.amount
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()


def get_orders( connection, current_user: int):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT  role
            FROM public.users
            WHERE id = %s
            """,
            (current_user,)
        )
        user = cursor.fetchone()
        if user is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )
        role = user[0]
        if role == "admin":
            cursor.execute(
                """
                SELECT id, user_id, product, amount
                FROM orders
                ORDER BY id
                """
            )
           
        else:
            cursor.execute(
                """
                SELECT id, user_id, product, amount
                FROM orders
                WHERE user_id = %s
                ORDER BY id
                """,
                (current_user,)
            )
        rows = cursor.fetchall()
        return [
            {
                "id": row[0],
                "user_id": row[1],
                "product": row[2],
                "amount": row[3]
            }
            for row in rows 
        ]

   

    finally:
        cursor.close()


def get_order(order_id, current_user, connection):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT o.id, o.user_id, o.product, o.amount,
            requester.role
            FROM orders o
            JOIN public.users requester ON requester.id = %s
            WHERE o.id = %s
            """,
            (current_user, order_id)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        order_id_db, owner_id, product, amount, role = row

        if role != "admin" and owner_id != current_user:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to access this order"
            )

        return {
            "id": order_id_db,
            "user_id": owner_id,
            "product": product,
            "amount": amount
        }

    finally:
        cursor.close()

def delete_order(order_id, current_user, connection):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT user_id
            FROM orders
            WHERE id = %s
            """,
            (order_id,)
        )

        result = cursor.fetchone()

        if result is None:
            return None

        owner_id = result[0]

        if owner_id != current_user:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to delete this order"
            )

        cursor.execute(
            """
            DELETE FROM orders
            WHERE id = %s
            RETURNING id
            """,
            (order_id,)
        )

        result = cursor.fetchone()

        if result is None:
            return None

        connection.commit()

        return result[0]

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()


        
def update_order(order_id, order, current_user, connection):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT user_id
            FROM orders
            WHERE id = %s
            """,
            (order_id,)
        )

        result = cursor.fetchone()

        if result is None:
            return None

        owner_id = result[0]

        if owner_id != current_user:
            raise HTTPException(
                status_code=403,
                detail="You are not allowed to modify this order"
            )

        cursor.execute(
            """
            UPDATE orders
            SET product = %s,
                amount = %s
            WHERE id = %s
            RETURNING id, user_id, product, amount
            """,
            (order.product, order.amount, order_id)
        )

        updated = cursor.fetchone()

        connection.commit()

        return {
            "id": updated[0],
            "user_id": updated[1],
            "product": updated[2],
            "amount": updated[3]
        }

    except Exception:
        connection.rollback()
        raise

    finally:
        cursor.close()