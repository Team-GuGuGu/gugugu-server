from fastapi import FastAPI, Request, HTTPException, BackgroundTasks, Depends
from fastapi.responses import JSONResponse
from api.main import router as api_router
from api.meal.usecase import MealUseCase
from db import init_db, get_session
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from dotenv import load_dotenv
import asyncio

#error
from api.models.exception import TokenException

load_dotenv()
app = FastAPI(title="async-fastapi-sqlalchemy")

app.include_router(api_router, prefix="/api")
loop = asyncio.get_event_loop()
background_tasks = BackgroundTasks()

# @app.post(path="/d/d/d/d/d")
async def periodic_task(
    # session: AsyncSession= Depends(get_session)
):
    session = get_session() 
    session = await session.__anext__()
    usecase = MealUseCase(session)
    while True:
        print("Running periodic task")
        await usecase.clear()
        await asyncio.sleep(21600) #6시간마다 초기화
@app.on_event("startup")
async def on_start():
    print("Setting to DB")
    await init_db()
    asyncio.create_task(periodic_task())
@app.get("/", include_in_schema=False)
async def health() -> JSONResponse:
    return JSONResponse({"message": "It worked!!"})

@app.exception_handler(TokenException)
async def token_exception_handler(request: Request, exc: TokenException):
    return JSONResponse(    
        status_code=exc.status,
        content={"status": exc.status, "message": exc.message, "data": exc.data}
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": exc.status_code, "message": exc.detail, "data": None}
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, log_level="info")
