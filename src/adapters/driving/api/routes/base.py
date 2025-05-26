from fastapi import APIRouter

router = APIRouter()


@router.get("/health_check", tags=["System"])
async def health_check():
    return {"status_code": 200, "status": "OK", "message": "Health check passed"}
