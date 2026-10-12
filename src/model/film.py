from typing import Optional

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, select

from src.database import Base

class Film_Model(Base):
    __tablename__="films"
    id: Mapped[int]=mapped_column(primary_key=True)
    title:Mapped[str]
    director:Mapped[Optional[str]]
    genre:Mapped[Optional[str]]
    year:Mapped[Optional[int]]
    rating:Mapped[Optional[int]]
    poster_path: Mapped[str | None] = mapped_column(String(500))

    
