from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import Base, sync_engine
from app.routes.author_route import router as authors_router
from app.routes.book_route import router as books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=sync_engine)

    yield

    sync_engine.dispose()


app = FastAPI(
    lifespan=lifespan,
)

cors_origins: list = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
)

app.include_router(books_router)
app.include_router(authors_router)
