from jose import jwt
from jose import JWTError

from fastapi import Depends
from fastapi import HTTPException

from fastapi.security import OAuth2PasswordBearer

from dotenv import load_dotenv

import os

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")

ALGORITHM = os.getenv("ALGORITHM")

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="users/login"
)


def get_current_user(
    token: str = Depends(
        oauth2_scheme
    )
):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        email = payload.get("sub")

        role = payload.get("role")

        user_id = payload.get("user_id")

        return {
            "id": user_id,
            "email": email,
            "role": role
        }

    except JWTError:

        raise HTTPException(
            status_code=401,
            detail="Invalid Token"
        )
    
