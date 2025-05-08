from fastapi import APIRouter, status
from api.v1.deps import token_dependency, get_me_usecase_dependency

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me")
async def get_me(token: token_dependency, get_me_usecase: get_me_usecase_dependency):
    return get_me_usecase.execute(token=token)
