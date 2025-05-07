from fastapi import APIRouter
from api.v1.endpoints.role import router as role_router
from api.v1.endpoints.auth import router as auth_router
from api.v1.endpoints.user import router as user_router

routers = APIRouter()
router_list = [auth_router, user_router, role_router]

for router in router_list:
    routers.include_router(router=router)
