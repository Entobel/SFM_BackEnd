from fastapi import APIRouter
from presentation.api.v1.endpoints import auth_endpoints, user_endpoints

routers = APIRouter()
router_list = [auth_endpoints.router, user_endpoints.router]

for router in router_list:
    routers.include_router(router=router)
