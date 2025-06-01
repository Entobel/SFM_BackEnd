from app.application.interfaces.use_cases.role.update_status_role_uc import \
    IUpdateStatusRoleUC
from app.core.exception import BadRequestError, NotFoundError
from app.domain.interfaces.repositories.role_repository import IRoleRepository


class UpdateRoleStatusUc(IUpdateStatusRoleUC):
    def __init__(self, role_repo: IRoleRepository):
        self.role_repo = role_repo

    def execute(self, role_id: int, is_active: bool):
        role = self.role_repo.get_role_by_id(role_id)

        if not role:
            raise NotFoundError(
                error_code="ETB-vai_tro_khong_ton_tai",
            )

        if role.is_active == is_active:
            return True

        if not is_active:
            is_in_use = self.role_repo.is_role_in_use(role=role)

            if is_in_use:
                raise BadRequestError(
                    error_code="ETB-vai_tro_dang_duoc_su_dung_khong_the_deactivate"
                )

        role.set_is_active(is_active=is_active)

        is_updated = self.role_repo.change_status_role(role)

        if not is_updated:
            raise BadRequestError(
                error_code="ETB-cap_nhat_trang_thai_vai_tro_that_bai",
            )

        return True
