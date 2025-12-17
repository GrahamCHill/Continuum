from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.internal import router as internal_router
from api.boards import router as boards_router
from infra.db import ensure_tables, get_db_connection

app = FastAPI(title="Continuum Kanban Module")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # controlled by gateway in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# INTERNAL endpoints (used only by core)
app.include_router(internal_router)

# PUBLIC module API (used by frontend)
app.include_router(boards_router, prefix="/api")


@app.on_event("startup")
def startup():
    conn = get_db_connection()
    ensure_tables(conn)
    conn.close()
