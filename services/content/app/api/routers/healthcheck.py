from fastapi import APIRouter

healthcheck_router = APIRouter(
    prefix="/api/v1",
    tags=["healthcheck"],
)


@healthcheck_router.get(
    "/health",
    summary="Проверить доступность API",
    description="Возвращет Ok, если API доступно",)
async def health() -> dict[str, str]:
    return {"status": "ok"}
