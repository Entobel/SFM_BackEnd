from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.grinding.create_grinding_uc import ICreateGrindingUC
from app.application.use_cases.grinding.create_grinding_uc_impl import CreateGrindingUC
from app.domain.interfaces.repositories.grinding_repository import IGrindingRepository
from app.infrastructure.database.repositories.grinding_repository_impl import GrindingRepository
from app.presentation.api.v1.dependencies.common_dependencies import CommonRepositoryDep, DatabaseDep, QueryHelperDep


def get_grinding_repository(
    db: DatabaseDep, query_helper: QueryHelperDep
) -> IGrindingRepository:
    return GrindingRepository(conn=db, query_helper=query_helper)


GrindingRepositoryDep = Annotated[IGrindingRepository, Depends(
    get_grinding_repository)]


def get_create_grinding_uc(grinding_repo: GrindingRepositoryDep, common_repo: CommonRepositoryDep, query_helper: QueryHelperDep) -> ICreateGrindingUC:
    return CreateGrindingUC(
        grinding_repo=grinding_repo,
        common_repo=common_repo,
        query_helper=query_helper
    )


CreateGrindingUCDep = Annotated[ICreateGrindingUC,
                                Depends(get_create_grinding_uc)]
