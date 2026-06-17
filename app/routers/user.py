from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from ..models import User
from ..dependencies import get_db

from ..auth import hash_password
from ..auth import verify_password
from ..auth import create_access_token

from ..security import get_current_user
from ..role_checker import admin_required

from ..schemas import (
    UserCreate,
    LoginSchema,
    UserUpdate
)

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


@router.post("/")
def create_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = User(
        name=user.name,
        email=user.email,
        password=hashed_password,
        role=user.role
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully"
    }


@router.post("/login")
def login(
    user: LoginSchema,
    db: Session = Depends(get_db)
):
    db_user = db.query(User).filter(
        User.email == user.email
    ).first()

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid Email"
        )

    if not verify_password(
        user.password,
        db_user.password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid Password"
        )

    token = create_access_token(
        {
            "sub": db_user.email,
            "role": db_user.role,
            "user_id": db_user.id
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }


@router.get("/")
def get_all_users(
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()

    return users


@router.get("/{user_id}")
def get_user(
    user_id: int,
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    return user


@router.put("/{user_id}")
def update_user(
    user_id: int,
    updated_user: UserUpdate,
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    existing_email = db.query(User).filter(
        User.email == updated_user.email,
        User.id != user_id
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="Email already exists"
        )

    user.name = updated_user.name
    user.email = updated_user.email
    user.role = updated_user.role

    db.commit()
    db.refresh(user)

    return {
        "message": "User Updated Successfully",
        "user": user
    }


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    current_user=Depends(admin_required),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.id == user_id
    ).first()

    if not user:
        raise HTTPException(
            status_code=404,
            detail="User not found"
        )

    db.delete(user)
    db.commit()

    return {
        "message": "User Deleted Successfully"
    }


@router.get("/me")
def get_me(
    current_user=Depends(get_current_user)
):
    return current_user