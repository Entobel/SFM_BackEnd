from core.database import db
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from infrastructure.database.repositories.role_repository import RoleRepository
from domain.services.role_service import RoleService
from domain.entities.role import Role
import logging

from sqlalchemy.orm import Session

router = APIRouter(prefix="/roles", tags=["Roles"])
logger = logging.getLogger("uvicorn")


def get_role_repository(db: Annotated[Session, Depends(db.get_db)]) -> RoleRepository:
    return RoleRepository(db)


def get_role_service(
    repo: Annotated[RoleRepository, Depends(get_role_repository)],
) -> RoleService:
    return RoleService(repo)


service_dependency = Annotated[RoleService, Depends(get_role_service)]


@router.get("/", status_code=status.HTTP_200_OK, response_model=List[Role])
async def get_all_roles(service: service_dependency):
    """
    Get all roles.
    """
    try:
        roles = service.get_all_roles()
        return roles
    except Exception as e:
        logger.error(f"[ROLE]:: Error retrieving roles: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve roles",
        )
