from fastapi import APIRouter
from presentation.api.v1.endpoints import (
    auth_endpoints,
    user_endpoints,
    department_endpoints,
    role_endpoints,
    factory_endpoints,
    shift_endpoints,
    diet_endpoints,
    production_object_endpoints,
    production_type_endpoints,
)

routers = APIRouter()
router_list = [
    auth_endpoints.router,
    user_endpoints.router,
    department_endpoints.router,
    role_endpoints.router,
    factory_endpoints.router,
    shift_endpoints.router,
    diet_endpoints.router,
    production_object_endpoints.router,
    production_type_endpoints.router,
]

for router in router_list:
    routers.include_router(router=router)
