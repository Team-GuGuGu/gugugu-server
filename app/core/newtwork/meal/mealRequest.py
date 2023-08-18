from ..base import BaseNetwork

from fastapi import HTTPException
from bs4 import BeautifulSoup
import json
from .parser import meal_parser

from typing import List
def timeCovert(timeCode: str) -> str:
    if timeCode == "1": return "breakfast"
    elif timeCode == "2": return "launch"
    else: return "dinner"


class MealRequest(BaseNetwork):
    def __init__(self, token: str) -> None:
        super().__init__()
        self.token = token

    async def searchMeal(self, YMD: str, schoolCode: str, local: str) -> List[dict]:
        # url = f"https://b2c-api-cdn.deeplol.gg/summoner/summoner?summoner_name={name}&platform_id=KR"
        # data, status = await self.httpGetRequests(url)
        # if status == 404:
        #     return errorResponse(404, "not found user")

        # return searchUserResponse(data)
        #https://open.neis.go.kr/hub/mealServiceDietInfo/?
        #Key=
        #Type=Json
        #MLSV_YMD=20230817
        #SD_SCHUL_CODE=7240454
        #ATPT_OFCDC_SC_CODE=D10
        url = f"https://open.neis.go.kr/hub/mealServiceDietInfo/?key={self.token}"+ "&Type=Json"+ f"&MLSV_YMD={YMD}"+ f"&SD_SCHUL_CODE={schoolCode}"+ f"&ATPT_OFCDC_SC_CODE={local}"
        data, status = await self.httpGetRequests(url)
        if type(data) is str:
            data = json.loads(data)

        result = []
        null = ["1", "2", "3"]

        if not data.get("RESULT"):
            for i in data["mealServiceDietInfo"][1]["row"]:
                menu, allergy = meal_parser(i["DDISH_NM"])
                result.append({
                    "menu": menu,
                    "allergy": allergy,
                    "calorie": i["CAL_INFO"],
                    "time": timeCovert(i["MMEAL_SC_CODE"])
                })
                del null[null.index(i["MMEAL_SC_CODE"])]
        for i in null:
            result.append({
                "menu": "존재하지 않습니다.",
                "allergy": "",
                "calorie": "0 Kcal",
                "time": timeCovert(i)
            })
        return result
    async def searchSchool(self, local: str, schoolName: str) -> List[dict]:
        url = f"https://open.neis.go.kr/hub/schoolInfo/?key={self.token}"+ "&Type=Json"+ f"&ATPT_OFCDC_SC_CODE={local}" + f"&SCHUL_NM={schoolName}"
        data, status = await self.httpGetRequests(url)
        if type(data) is str:
            data = json.loads(data)

        if data.get("RESULT"):
            print(data)
            return HTTPException(404, detail="not found school")
        result = []
        for i in data["schoolInfo"][1]["row"]:
            result.append({
                "schoolCode": i["SD_SCHUL_CODE"],
                "schoolName": i["SCHUL_NM"]
            })
        return result
