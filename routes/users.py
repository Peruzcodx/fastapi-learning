from fastapi import APIRouter, Depends, HTTPException
from schemas.user import User, UserCreate, UserUpdate
from database import get_db
from services.user_services import get_user_by_email, register_user
from schemas.user import  LoginRequest, RefreshTokenRequest, UserCreate
from security import get_current_user, require_admin
from services.user_services import (
    get_user,
    update_user,
    delete_user,
    get_users,
    


)

router = APIRouter()


@router.get("/users", response_model=list[User])
def all_users(connection=Depends(get_db)):
    return get_users(connection)


@router.get("/users/{user_id}", response_model=User)
def get_user_route(user_id: int, connection=Depends(get_db)):
    return get_user(user_id, connection)




@router.patch("/users/{user_id}", response_model=User)
def update_user_route(
    user_id: int,
    user: UserUpdate,
    connection=Depends(get_db)
):
    return update_user(user_id, user, connection)


@router.delete("/users/{user_id}")
def delete_user_route(
    user_id: int,
    current_user: int = Depends(require_admin),
    connection=Depends(get_db)
):
    return delete_user(user_id, connection)


@router.get("/me")
def get_my_profile(
    current_user: int = Depends(get_current_user),
    connection=Depends(get_db)
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, city, email
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

        return {
            "id": user[0],
            "name": user[1],
            "city": user[2],
            "email": user[3]
        }

    finally:
        cursor.close()
@router.post("/register", status_code=201)
def register(
    user: UserCreate,
    connection=Depends(get_db)
):
    try:
        new_user = register_user(user, connection)

        return {
            "message": "User registered successfully",
            "user": {
                "id": new_user[0],
                "name": new_user[1],
                "city": new_user[2],
                "email": new_user[3],
                "role": new_user[4]
            }
        }

    except ValueError as e:
        raise HTTPException(
            status_code=409,
            detail=str(e)
        )