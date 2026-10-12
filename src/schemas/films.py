from pydantic import BaseModel
from typing import Optional

class Film_add_scheme(BaseModel):
    title: str 
    director:Optional[str]=None
    genre:Optional[str]=None
    year:Optional[int]=None
    rating:Optional[int]=None



class Film_scheme(Film_add_scheme):
    id:int
    poster_path: Optional[str]=None

    class Config:
        from_attributes = True

class Film_update_scheme(BaseModel):
    title: Optional[str]=None
    director:Optional[str]=None
    genre:Optional[str]=None
    year:Optional[int]=None
    rating:Optional[int]=None

class Film_filters_scheme(BaseModel):
    director: Optional[str]=None
    genre: Optional[str]=None
    year_from: Optional[int]=None
    year_to: Optional[int]=None
    desc_find: Optional[str]=None
    asc_find: Optional[str]=None


