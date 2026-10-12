from typing import Annotated
import os
import shutil
from fastapi import APIRouter, Depends,HTTPException, Query, UploadFile
from sqlalchemy import select
from src.api.repository import FilmsRepo
from src.api.dependencies import SessionDep
from src.database import engine, Base
from src.schemas.films import Film_add_scheme, Film_filters_scheme,Film_scheme, Film_update_scheme
from src.model.film import Film_Model
from src.api.dependencies import PaginationDep

from src.database import new_session

router=APIRouter()

UPLOAD_DIR="uploads"

@router.post("/setup_database")
async def setup_database():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    return {"ok": True, "message": "Database setup completed successfully"}

# @router.post("/films")
# async def add_film(data: Film_add_scheme,session: SessionDep):
#     new_film= Film_Model(
#         title=data.title,
#         director=data.director,
#     )
#     session.add(new_film)
#     await session.commit()


@router.post("/films")
async def add_film(
    data: Annotated[Film_add_scheme,Depends()]
    ) -> dict:
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
async def upload_poster(film_id: int, file: UploadFile):
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
