from __future__ import annotations

from sqlalchemy.orm import Mapped, mapped_column, relationship, selectinload
from sqlalchemy import String, select
from typing import TYPE_CHECKING, AsyncIterator
from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base

class MealTable(Base):
    __tablename__ = "meal"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    date: Mapped[str] = mapped_column(nullable=False, unique=True)# yyyy-MM-dd
    local: Mapped[str] = mapped_column(nullable=False)# local Code
    school: Mapped[str] = mapped_column(nullable=False)# school code
    meal: Mapped[str] = mapped_column(nullable=False)# meal list(json.loads, json.dumps)