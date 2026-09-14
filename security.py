import jwt
from config import SECRET_KEY
from database import get_db
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta, timezone

from fastapi import Depends, HTTPException


if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not configured")
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def create_access_token(user_id: int):
    expires = datetime.now(timezone.utc) + timedelta(minutes=15)
    expires = int(expires.timestamp())
    payload = {
        "user_id": user_id,
        "type" : "access",
        "exp": expires
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_access_token(token: str):
    payload = jwt.decode(
        token,
        SECRET_KEY,
        algorithms=[ALGORITHM]
    )
    return payload


def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = verify_access_token(token)
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )
        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid token"
            )

        return user_id

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid token"
        )
def require_admin(
    current_user: int = Depends(get_current_user),
    connection=Depends(get_db)
):
    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT role
            FROM public.users
            WHERE id = %s
            """,
            (current_user,)
        )

        result = cursor.fetchone()

        if result is None:
            raise HTTPException(
                status_code=404,
                detail="User not found"
            )

        role = result[0]

        if role != "admin":
            raise HTTPException(
                status_code=403,
                detail="Admin access required"
            )

        return current_user

    finally:
        cursor.close()        


def create_refresh_token(user_id: int):
    expires = datetime.now(timezone.utc) + timedelta(days=7)
    expires = int(expires.timestamp())
    payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": expires
    }

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return token

def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        user_id = payload.get("user_id")

        if user_id is None:
            raise HTTPException(
                status_code=401,
                detail="Invalid refresh token"
            )

        return user_id

    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid refresh token"
        )