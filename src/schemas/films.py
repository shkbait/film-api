from pydantic import BaseModel
from typing import Optional
from pydantic import Field

class Film_add_scheme(BaseModel):
    title: str 
    director:Optional[str]=None
    genre:Optional[str]=None
    year:Optional[int]=Field(None,ge=1)
    rating:Optional[int] = Field(None,ge=1,le=10)



class Film_scheme(Film_add_scheme):
    id:int
    poster_path: Optional[str]=None

    class Config:
        from_attributes = True

class Film_update_scheme(BaseModel):
    title: Optional[str]=None
    director:Optional[str]=None
    genre:Optional[str]=None
    year:Optional[int]=Field(None,ge=1)
    rating:Optional[int]=Field(None,ge=1,le=10)

class Film_filters_scheme(BaseModel):
    director: Optional[str]=None
    genre: Optional[str]=None
    year_from: Optional[int]=None
    year_to: Optional[int]=None
    desc_find: Optional[str]=None
    asc_find: Optional[str]=None

class User_Reg_sheme(BaseModel):
    username: str
    password: str

class UserLoginScheme(BaseModel):
    username: str
    password: str
