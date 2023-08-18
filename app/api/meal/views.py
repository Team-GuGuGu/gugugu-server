from fastapi import APIRouter, Depends, Path, Request, HTTPException

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from api.models import baseResponse
from db import get_session
from .usecase import MealUseCase

from core.newtwork.meal.mealRequest import MealRequest
import json
import os
token = os.environ.get("TOKEN")
router = APIRouter(prefix="/meal")
network = MealRequest(token)
@router.get("/get")
async def getMeal(
    request: Request,
    local: str,
    date: str,
    schoolCode: str,
    session: AsyncSession = Depends(get_session)
):
    get_session()
    print(type(session))
    usecase = MealUseCase(session)
    result = await usecase.readBySchool(
        local=local,
        date=date,
        school=schoolCode
    )
    if result != False:
        result = result[0]
        return baseResponse(
            data=json.loads(result.meal.encode().decode())
        )
    data = await network.searchMeal(
        YMD=date,
        schoolCode=schoolCode,
        local=local
    )
    #기록
    if data["success"] is True:
        await usecase.create(local=local, date=date, school=schoolCode, meal=data["data"])
    return baseResponse(data=data["data"])
@router.get("/school")
async def getSchool(
    request: Request,
    schoolName: str,
    local: str,
    session: AsyncSession = Depends(get_session)
):
    data = await network.searchSchool(local=local, schoolName=schoolName)
    return baseResponse(data=data)
    ""

"""https://open.neis.go.kr/hub/mealServiceDietInfo/?Key=4f979b8710484c0989446ed486f3e178&Type=Json&MLSV_YMD=20230817&SD_SCHUL_CODE=7240454&ATPT_OFCDC_SC_CODE=D10/Users/dgsw8th13/Desktop/app/core/network/base.py"""