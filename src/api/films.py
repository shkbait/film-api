from typing import Annotated
import os
import shutil
from pydantic import BaseModel,Field,EmailStr,ConfigDict
from fastapi import APIRouter, Depends,HTTPException, Query, Request, Response, UploadFile,Header
from sqlalchemy import select
from src.api.repository import FilmsRepo
from src.api.dependencies import SessionDep
from src.database import engine, Base
from src.user_database import engine as user_engine
from src.user_database import Base as user_base
from src.schemas.films import Film_add_scheme, Film_filters_scheme,Film_scheme, Film_update_scheme, UserLoginScheme, User_Reg_sheme
from src.model.film import Film_Model
from src.model.auth import Login_Model
from src.api.dependencies import PaginationDep
from authx import TokenPayload
from src.api.repository import security,config


from src.database import new_session

router=APIRouter()

UPLOAD_DIR="uploads"


@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True, "message": "Database setup completed successfully"}

@router.post("/setup_user_database")
async def setup_user_db():
    async with user_engine.begin() as conn:
        await conn.run_sync(user_base.metadata.create_all)
    return {"ok": True, "message": "Database setup completed successfully"}


# @router.post("/films")
# async def add_film(data: Film_add_scheme,session: SessionDep):
#     new_film= Film_Model(
#         title=data.title,
#         director=data.director,
#     )
#     session.add(new_film)
#     await session.commit()

# @router.get("/profile")
# async def profile(
#     payload: TokenPayload = Depends(security.access_token_required)
# ):
#     return {"user_id": payload.sub}

# @router.get("/check-cookie")
# async def check_cookie(request: Request):
#     return {
#         "access_cookie": request.cookies.get("my_access_token"),
#         "csrf_cookie": request.cookies.get("csrf_access_token")
#     }

@router.post("/films")
async def add_film(
    data: Annotated[Film_add_scheme,Depends()],
    ) -> dict:

    # if data.year is not None:
    #     if data.year<1:
    #         raise HTTPException(status_code=422, detail="incorrect year")
    # if data.rating is not None:
    #     if data.rating<1 or data.rating>10:
    #         raise HTTPException(status_code=422, detail="incorrect rating")
    film_id = await FilmsRepo.add_one(data)
    return {"ok": True, "film_id": film_id}


# @router.post("/films/{film_id}/upload-poster")
# async def upload_poster(film_id: int, file: UploadFile):
#     file_ext=os.path.splitext(file.filename)[1]
#     file_name=f"poster_{film_id}{file_ext}"
#     file_path=os.path.join(UPLOAD_DIR, file_name)

#     os.makedirs(UPLOAD_DIR, exist_ok=True)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
#     async with new_session() as session:
#         result=await session.execute(select(Film_Model).where(Film_Model.id==film_id))
#         film=result.scalar_one_or_none()
#         if not film:
#             raise HTTPException(status_code=404, detail="film not found")
#         film.poster_path=file_path
#         await session.commit()
#     return {"message": "Successfully", "path": file_path}

@router.post("/films/{film_id}/upload-poster")
async def upload_poster(film_id: int, file: UploadFile,):
    if not file.filename:
        raise HTTPException(status_code=400, detail="file withot name")
    result= await FilmsRepo.upload_poster(film_id,file)
    if result is None:
    # if not result:
        raise HTTPException(status_code=404, detail="film not found")
    return {"ok": True, "message": "Successfully"}



@router.get("/films/filters")
async def get_current_films(
    pagination: PaginationDep,
    # payload: TokenPayload = Depends(security.access_token_required),
    title: str | None = None,   
    genre: str | None = None,
    director: str | None = None,
    year_from: int | None = None,
    year_to: int | None = None,
    desc_find: bool = False,
    asc_find: bool = False,

) -> list[Film_scheme]:
    films = await FilmsRepo.current_find(title, genre, director, year_from, year_to, desc_find, asc_find)
    return films[pagination.offset : pagination.offset + pagination.limit]

@router.get("/films/{film_id}")
async def get_film_or_404(film_id: int)->Film_scheme:
    result = await FilmsRepo.find_one(film_id)
    if result is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return Film_scheme.model_validate(result, from_attributes=True)


@router.patch("/films/{film_id}")
async def update(film_id: int, data: Annotated[Film_update_scheme,Depends()])->Film_scheme:
    film = await FilmsRepo.update(film_id, data)
    if film is None:
        raise HTTPException(status_code=404, detail="Film not found")
    return film

@router.delete("/films/{film_id}")
async def delete_f(film_id: int)->dict:
    deleted = await FilmsRepo.delete_film(film_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Film not found")
    return {"ok": True}


# @router.post("/Uploadfiles")
# def create_upload_files(uploadedfiles: list[UploadFile]):
#     for uploadedfile in uploadedfiles:
#         file=uploadedfile.file
#         filename=uploadedfile.filename
#         with open(f"_1{filename}","wb") as f:
#             f.write(file.read())

# @router.get("/films")
# async def get_films(
#     pagination: PaginationDep 
# ) -> list[Film_scheme]:

#     films = await FilmsRepo.find_all()
    
#     return films[pagination.offset : pagination.offset + pagination.limit]

# @router.get("/films/sort")
# async def sort_films(
#     year_from_desc: int | None = None,
#     year_from_asc: int | None = None,
#     year_to_desc: int | None = None,
#     year_to_asc: int | None = None,
#     )->list[Film_scheme]:
#     films=await FilmsRepo.sort_films(year_from_desc,year_from_asc,year_to_desc,year_to_asc)
#     return films
