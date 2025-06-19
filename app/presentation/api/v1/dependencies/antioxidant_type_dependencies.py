from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.antioxidant_type.list_antioxidant_type_uc import IListAntioxidantTypeUC
from app.application.use_cases.antioxidant_type.list_antioxidant_type_uc_impl import ListAntioxidantTypeUC
from app.domain.interfaces.repositories.antioxidant_type_repository import IAntioxidantTypeRepository
from app.infrastructure.database.repositories.antioxidant_type_repository_impl import AntioxidantTypeRepository
from app.presentation.api.v1.dependencies.common_dependencies import DatabaseDep, QueryHelperDep


def get_antioxidant_type_repository(conn: DatabaseDep, query_helper: QueryHelperDep) -> IAntioxidantTypeRepository:
    return AntioxidantTypeRepository(conn=conn, query_helper=query_helper)


AntioxidantTypeRepositoryDep = Annotated[IAntioxidantTypeRepository, Depends(
    get_antioxidant_type_repository)]


def get_list_antioxidant_type_uc(antioxidant_type_repository: AntioxidantTypeRepositoryDep) -> IListAntioxidantTypeUC:
    return ListAntioxidantTypeUC(
        antioxidant_repo=antioxidant_type_repository
    )


ListAntioxidantTypeUseCaseDep = Annotated[IListAntioxidantTypeUC, Depends(
    get_list_antioxidant_type_uc)]
