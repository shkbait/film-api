from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker,AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine=create_async_engine('sqlite+aiosqlite:///./users.db')
#создание подключения указывет на работы с файлом фильмы 
new_session=async_sessionmaker(engine,expire_on_commit=False)
#создает окно (сессию) для работы с базой указывает что нужно рабоать с движком и запрещает стирать данные
async def get_session():
    async with new_session() as session:
        yield session

class Base(DeclarativeBase):
    pass