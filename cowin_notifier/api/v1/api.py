from fastapi.routing import APIRouter

from cowin_notifier.api.v1.watch.views import router as logs_router

router = APIRouter()

router.include_router(logs_router, prefix="/watch", tags=["watcher"])
