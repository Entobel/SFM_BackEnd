from domain.interfaces.repositories.zone_repository import IZoneRepository
from infrastructure.database.repositories.zone_repository_impl import \
    ZoneRepository
from presentation.api.v1.dependencies.common_dependencies import (
    DatabaseDep, QueryHelperDep)


def get_zone_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IZoneRepository:
    return ZoneRepository(conn=db, query_helper=query_helper)
