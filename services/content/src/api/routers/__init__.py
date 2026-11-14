from .films import film_router
from .genres import genre_router
from .healthcheck import healthcheck_router
from .persons import person_router


__all__ = (
    "film_router",
    "genre_router",
    "healthcheck_router",
    "person_router",
)
