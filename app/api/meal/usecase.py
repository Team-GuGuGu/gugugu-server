from db import AsyncSession
from sqlalchemy import select
from api.models import MealTable
from typing import Tuple, List
from fastapi import HTTPException
import json


class MealUseCase:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session= session
    async def readBySchool(self, local: str, date: str, school: str) -> MealTable | bool:
        async with self.async_session() as session:
            _query = select(MealTable).filter(MealTable.local == local, MealTable.date == date, MealTable.school == MealTable.school)
            _result = (await session.execute(_query)).scalars().all()
            print(_result)
            if not _result:
                return False
            return _result
    async def create(self, local: str, date: str, school: str, meal: list):
        async with self.async_session() as session:
            _table = MealTable(local=local, date=date, school=school, meal=json.dumps(meal))
            session.add(_table)
            try:
                await session.commit()
            except:
                raise HTTPException(404, detail="what happend..?")
            return True
    async def clear(self):
        async with self.async_session() as session:
            await session.execute(MealTable.__table__.delete())
            await session.commit()
            # _table = (await session.execute(select(MealTable)).scalars().first())
            # if _table:
            #     await session.delete(_table)
            #     await session.commit()

