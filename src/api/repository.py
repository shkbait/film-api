from pathlib import Path

from fastapi import Depends, UploadFile
import os
import shutil
from sqlalchemy import select,desc
from src.database import new_session
from src.model.film import Film_Model
from src.schemas.films import Film_add_scheme, Film_filters_scheme,Film_scheme, Film_update_scheme
import pandas as pd
UPLOAD_DIR="uploads"


class FilmsRepo:
 @classmethod
 async def add_one(cls, data: Film_add_scheme) -> int:

        async with new_session() as session:

            film_dict = data.model_dump()
            
          
            new_film = Film_Model(**film_dict)
            
            # Добавляем в сессию
            session.add(new_film)
            
           
            await session.flush()
           
            await session.commit()
            
            return new_film.id

#  @classmethod
#  async def upload_poster(cls,film_id:int, file: UploadFile)->bool:
#       async with new_session() as session:
#            file_ext=os.path.splitext(file.filename)[1]
#            file_name=f"poster{film_id}{file_ext}"
#            file_path=os.path.join(UPLOAD_DIR, file_name)
#            os.makedirs(UPLOAD_DIR, exist_ok=True)
#            with open(file_path, "wb") as buffer:
#                 shutil.copyfileobj(file.file,buffer)
#            result=await session.execute(select(Film_Model).where(Film_Model.id==film_id))
#            film=result.scalars().one_or_none()
#            film.poster_path=file_path
#            await session.commit()
#            if film is None:
#                 return False
#            return True
           
 @classmethod
 async def upload_poster(cls, film_id: int, file: UploadFile) -> bool:
    async with new_session() as session:
        result = await session.execute(select(Film_Model).where(Film_Model.id == film_id))
        film = result.scalars().one_or_none()
        if film is None:
            return False
        file_ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
        file_name = f"poster_{film_id}{file_ext}"
        file_path = os.path.join(UPLOAD_DIR, file_name)
        
        os.makedirs(UPLOAD_DIR, exist_ok=True)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        film.poster_path = file_path
        await session.commit()
        return True

#  @classmethod
#  async def csv_read(file_path: str):
#       async with new_session() as session:
#            csv_op=pd.read_csv(file_path)
#            records=csv_op.to_dict(orient="records")
 

 @classmethod
 async def find_one(cls, film_id: int) -> Film_scheme | None:
      async with new_session() as session:
           query=select(Film_Model).where(Film_Model.id == film_id)
           result=await session.execute(query)
           film_model=result.scalars().one_or_none()
           if film_model is None:
                return None
           return Film_scheme.model_validate(film_model, from_attributes=True)
 @classmethod
 async def current_find(cls,title: str | None, genre: str | None, director: str | None, year_from: int | None, year_to: int | None, desc_find: bool, asc_find: bool)->list[Film_scheme]:
      async with new_session() as session:
           query=select(Film_Model)#.where(Film_Model.genre=="")
           if title is not None:
                query=query.where(Film_Model.title.ilike(f"%{title}%"))
           if genre is not None:
                # query=query.where(Film_Model.genre==genre)
                query=query.where(Film_Model.genre.ilike(f"%{genre}%"))
           if director is not None:
                query=query.where(Film_Model.director.ilike(f"%{director}%"))
           if year_from is not None:
                query=query.where(Film_Model.year >= year_from)
           if year_to is not None:
                query=query.where(Film_Model.year <= year_to)
           if desc_find is True:
                query=query.order_by(Film_Model.year.desc())
           if asc_find is True:
                query=query.order_by(Film_Model.year.asc())
           result = await session.execute(query)
           film_models= result.scalars().all()
           return [
                Film_scheme.model_validate(film, from_attributes=True)
                for film in film_models
           ]
 @classmethod
 async def sort_films(cls,year_from_desc: int, year_from_asc: int, year_to_desc: int, year_to_asc:int)->list[Film_scheme]:
      async with new_session() as session:
        #    query=select(Film_Model, year_desc, year_asc).order_by(Film_Model.year.desc())
        #    query=select(Film_Model).order_by(Film_Model.year_from.desc())
           if year_from_desc is not None:
                query=select(Film_Model, year_from_desc).where(Film_Model.year<=year_from_desc).order_by(Film_Model.year.desc())
           if year_from_asc is not None:
                query=select(Film_Model, year_from_asc).where(Film_Model.year<=year_from_asc).order_by(Film_Model.year.asc())
           if year_to_desc is not None:
                query=select(Film_Model, year_to_desc).where(Film_Model.year>=year_to_desc).order_by(Film_Model.year.desc())
           if year_to_asc is not None:
                query=select(Film_Model, year_to_asc).where(Film_Model.year>=year_to_asc).order_by(Film_Model.year.asc())
           result = await session.execute(query)
           sort_models = result.scalars().all()

           return [
                Film_scheme.model_validate(film, from_attributes=True)
                for film in sort_models
           ]


 @classmethod
 async def find_all(cls) -> list[Film_scheme]:

        async with new_session() as session:
            query = select(Film_Model)
            
          
            result = await session.execute(query)
            film_models = result.scalars().all()
            
     
            film_schemas = [
                Film_scheme.model_validate(film_model, from_attributes=True)
                for film_model in film_models
            ]
            return film_schemas

 @classmethod
 async def update(cls, film_id: int, data: Film_update_scheme):
      async with new_session() as session:
           film=await session.get(Film_Model, film_id)
           if film is None:
                return None
           for field, value in data.model_dump(exclude_unset=True).items():
                setattr(film, field, value) #{film, "rating", 9}==film.rating=9
           await session.commit()
           return Film_scheme.model_validate(film, from_attributes=True)
           
 @classmethod
 async def delete_film(cls,film_id: int)->bool:
      async with new_session() as session:
           film=await session.get(Film_Model,film_id)    
           if film is None:
                return False
           if film.poster_path is not None:
                Path(film.poster_path).unlink(missing_ok=True)
           await session.delete(film)
           await session.commit()
           return True
           
