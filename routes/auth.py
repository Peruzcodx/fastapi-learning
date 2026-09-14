from fastapi import APIRouter, Depends, HTTPException
from database import get_db
from schemas.user import  RefreshTokenRequest
from pwdlib import PasswordHash
from security import create_access_token,create_refresh_token, verify_refresh_token
from fastapi.security import OAuth2PasswordRequestForm
router = APIRouter(
    prefix="/auth",
    tags=["Authentications"]
)

password_hash = PasswordHash.recommended()


@router.post("/login")
def login(user: OAuth2PasswordRequestForm = Depends(), connection=Depends(get_db)):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT id, name, email, password_hash
            FROM public.users
            WHERE email = %s
            """,
            (user.username,)
        )

        result = cursor.fetchone()

        if result is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        stored_hash = result[3]

        if not password_hash.verify(user.password, stored_hash):
            raise HTTPException(
                status_code=401,
                detail="Invalid email or password"
            )

        access_token = create_access_token(result[0])
        refresh_token = create_refresh_token(result[0])
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

    finally:
        cursor.close()
@router.post("/refresh")
def refresh_token(data :RefreshTokenRequest):
    user_id = verify_refresh_token(data.refresh_token)
    new_access_token = create_access_token(user_id)
    return{
        "access_token": new_access_token,
        "token_type": "bearer"
    }