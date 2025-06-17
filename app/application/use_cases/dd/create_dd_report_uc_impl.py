from loguru import logger
from app.application.interfaces.use_cases.dd.create_dd_report_uc import ICreateDDReportUC
from app.domain.interfaces.repositories.common_repository import ICommonRepository
from app.domain.interfaces.repositories.dd_repository import IDDRepository
from app.domain.interfaces.services.query_helper_service import IQueryHelperService


class CreateDDReportUC(ICreateDDReportUC):
    def __init__(self, dd_repository: IDDRepository, common_repository: ICommonRepository, query_helper: IQueryHelperService):
        self.dd_repository = dd_repository
        self.common_repository = common_repository
        self.query_helper = query_helper

    def execute(self, dd_dto):
        logger.debug(f"DATA: {dd_dto}")
