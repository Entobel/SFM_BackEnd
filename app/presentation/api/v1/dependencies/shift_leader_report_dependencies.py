from typing import Annotated

from fastapi import Depends
from app.application.interfaces.use_cases.shift_leader_report.create_shift_leader_report_uc import (
    ICreateShiftLeaderReportUC,
)
from app.application.use_cases.shift_leader_report.create_shift_leader_report_uc_impl import (
    CreateShiftLeaderReportUC,
)
from app.domain.interfaces.repositories.shift_leader_report_repository import (
    IShiftLeaderReportRepository,
)
from app.infrastructure.database.repositories.shift_leader_report_repository_impl import (
    ShiftLeaderReportRepositoryImpl,
)
from app.presentation.api.v1.dependencies.common_dependencies import (
    CommonRepositoryDep,
    DatabaseDep,
    QueryHelperDep,
)


def get_shift_leader_repository(
    conn: DatabaseDep, query_helper: QueryHelperDep
) -> IShiftLeaderReportRepository:
    return ShiftLeaderReportRepositoryImpl(conn=conn, query_helper=query_helper)


ShiftLeaderRepositoryDep = Annotated[
    IShiftLeaderReportRepository, Depends(get_shift_leader_repository)
]


def get_create_shift_leader_report_uc(
    shift_leader_report_repository: ShiftLeaderRepositoryDep,
    common_repository: CommonRepositoryDep,
    query_helper: QueryHelperDep,
) -> ICreateShiftLeaderReportUC:
    return CreateShiftLeaderReportUC(
        shift_leader_report_repository=shift_leader_report_repository,
        common_repository=common_repository,
        query_helper=query_helper,
    )


CreateShiftLeaderReportUCDep = Annotated[
    ICreateShiftLeaderReportUC, Depends(get_create_shift_leader_report_uc)
]
