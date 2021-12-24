from typing import Any, Generic, Optional, Type, TypeVar

from sqlalchemy import select

from db.session import Base, SessionManager

ModelType = TypeVar('ModelType', bound=Base)


class DaoBase(Generic[ModelType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.db = SessionManager()

    async def get(self, id: Any) -> Optional[ModelType]:
        sql_stmt = select(self.model).where(self.model.id == id)
        async with self.db.obtain_session() as sess:
            result = (await sess.execute(sql_stmt)).scalar_one_or_none()
        return result
