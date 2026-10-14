from typing import Annotated

from fastapi import APIRouter, Depends, Response
from pwdlib import PasswordHash
from src.api.repository import security
from src.schemas.films import User_Reg_sheme,UserLoginScheme
from src.api.repository import FilmsRepo
from src.api import router
from src.model.auth import Login_Model
from src.api.repository import config

password_hash = PasswordHash.recommended()

# def hash_password(password: str) -> str:
#     return password_hash.hash(password)

# def verify_password(password: str, hashed_password: str) -> bool:
#     return password_hash.verify(password, hashed_password)

router=APIRouter()

@router.post("/Registration")
async def reg_user(
    data: Annotated[User_Reg_sheme, Depends()]
    )->dict:
    user_id= await FilmsRepo.registration(data)
    return {"ok": True, "id": user_id}

@router.post("/Login")
async def login_user(
    data: Annotated[UserLoginScheme,Depends()],
    response: Response
    )->dict:
    return await FilmsRepo.login(data, response)

@router.post("/Logout")
async def logout_user(
    response: Response,
    ):
    response.delete_cookie(config.JWT_ACCESS_COOKIE_NAME)
    return {"ok": True}

from fastapi import Request, HTTPException, status

