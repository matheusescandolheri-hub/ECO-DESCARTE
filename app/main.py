from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import SessionLocal, init_db
from app.routes import api, web
from app.seed import seed_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()

    yield


app = FastAPI(
    title="EcoDescarta",
    description="Sistema web para orientação de descarte consciente de resíduos.",
    version="0.1.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(web.router)
app.include_router(api.router)

