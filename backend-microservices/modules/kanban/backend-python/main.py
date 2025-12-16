from fastapi import FastAPI

app = FastAPI()

from api.internal import router as internal_router  # noqa
from api.boards import router as boards_router      # noqa

app.include_router(internal_router)
app.include_router(boards_router, prefix="/api")
