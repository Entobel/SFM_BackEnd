from fastapi import APIRouter


router = APIRouter(prefix="/roles", tags=["Role"])


@router.get("/")
async def get_all_roles():
    pass


@router.post("/")
async def create_role():
    pass


@router.put("/")
async def update_role():
    pass


@router.delete("/")
async def delete_role():
    pass
