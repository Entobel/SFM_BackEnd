from fastapi import APIRouter, status

router = APIRouter(prefix="/users", tags=["User"])


@router.get("/test", status_code=status.HTTP_200_OK)
async def check_connection():
    return {"message": "ok"}
