from fastapi import APIRouter

from app.presentation.api.v1.endpoints import (auth_endpoints,
                                               department_endpoints,
                                               diet_endpoints, factory_endpoints,
                                               growing_endpoints,
                                               production_object_endpoints,
                                               production_type_endpoints,
                                               role_endpoints, shift_endpoints,
                                               user_endpoints, zone_endpoints, level_endpoints)

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
    growing_endpoints.router,
    zone_endpoints.router,
    level_endpoints.router,
]

for router in router_list:
    routers.include_router(router=router)
