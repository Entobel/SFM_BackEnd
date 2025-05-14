from fastapi import APIRouter


router = APIRouter(prefix="/roles", tags=["Role"])


@router.get("/", response_model_exclude_none=True)
async def get_all_roles():
    pass


@router.post("/", response_model_exclude_none=True)
async def create_role():
    pass


@router.put("/", response_model_exclude_none=True)
async def update_role():
    pass


@router.delete("/", response_model_exclude_none=True)
async def delete_role():
    pass
