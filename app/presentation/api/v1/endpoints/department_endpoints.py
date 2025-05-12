from fastapi import APIRouter


router = APIRouter(prefix="/departments", tags=["Department"])


@router.get("/")
async def get_all_department():
    pass


@router.post("/")
async def create_department():
    pass


@router.put("/")
async def update_department():
    pass


@router.delete("/")
async def create_department():
    pass
