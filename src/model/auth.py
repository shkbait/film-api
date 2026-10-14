from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String
from src.user_database import Base

class Login_Model(Base):
    __tablename__="Users"
    id: Mapped[int]=mapped_column(primary_key=True)
    username: Mapped[str]=mapped_column(String(50), unique=True)
    password: Mapped[str]=mapped_column(String(255))