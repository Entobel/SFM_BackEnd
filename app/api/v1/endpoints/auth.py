from fastapi import APIRouter, status

router = APIRouter(prefix="/auth", tags=["Authentication"])

# Login route
