from fastapi import APIRouter

from app.presentation.api.v1.endpoints import (
    auth_endpoints,
    department_endpoints,
    diet_endpoints,
    factory_endpoints,
    operation_type_endpoints,
    product_type_endpoints,
    role_endpoints,
    shift_endpoints,
    user_endpoints,
    zone_endpoints,
    level_endpoints,
    growing_endpoints,
    harvesting_endpoints,
    grinding_endpoints,
    dd_endpoints,
    vfbd_endpoints,
    dryer_machine_type_endpoints,
    dryer_product_type_endpoints,
    dried_larvae_discharge_type_endpoints,
    antioxidant_type_endpoints,
    packing_type_endpoints
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
    product_type_endpoints.router,
    operation_type_endpoints.router,
    zone_endpoints.router,
    level_endpoints.router,
    growing_endpoints.router,
    harvesting_endpoints.router,
    grinding_endpoints.router,
    dd_endpoints.router,
    vfbd_endpoints.router,
    dryer_machine_type_endpoints.router,
    dryer_product_type_endpoints.router,
    dried_larvae_discharge_type_endpoints.router,
    antioxidant_type_endpoints.router,
    packing_type_endpoints.router
]

for router in router_list:
    routers.include_router(router=router)
