from fastapi import APIRouter
from .meal.views import router as meal_router
router = APIRouter()
router.include_router(meal_router)