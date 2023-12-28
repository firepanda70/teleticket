from fastapi import APIRouter

from .user import user_router
from .message import message_router
from .ticket import ticket_router

v1_router = APIRouter(prefix='/v1')

v1_router.include_router(user_router)
v1_router.include_router(message_router)
v1_router.include_router(ticket_router)
