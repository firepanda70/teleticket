from fastapi.routing import APIRouter

from .api import api_router
from .web import web_router

main_router = APIRouter()

main_router.include_router(api_router)
main_router.include_router(web_router, include_in_schema=False)
