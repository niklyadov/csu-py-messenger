from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from crud.user import authenticate
import crud.user as crud
from deps import get_db, get_current_user
from schemas.user import UserInDB, UserCreate
from security import create_access_token

router = APIRouter(prefix="/auth")


@router.post("/login")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db=Depends(get_db),
):
    """Login"""
    user = authenticate(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Username or password incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(user_id=user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register", response_model=UserInDB)
async def create_user(user: UserCreate, db=Depends(get_db)):
    """Registration"""
    result = crud.create_user(db=db, user=user)

    return result


@router.post("/refresh")
async def refresh_access_token(user_id=Depends(get_current_user)):
    access_token = create_access_token(user_id=user_id)
    return {"access_token": access_token, "token_type": "bearer"}
