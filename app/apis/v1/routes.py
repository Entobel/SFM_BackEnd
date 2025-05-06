from fastapi import APIRouter
from .enpoints.auth import router as auth_router
from .enpoints.user import router as user_router

routers = APIRouter()
router_list = [auth_router, user_router]

for router in router_list:
    routers.include_router(router=router)
