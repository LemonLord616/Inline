import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from database import init_db
from routes import api_router, pages_router
from tasks import background_loop


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    task = asyncio.create_task(background_loop())
    yield
    task.cancel()


app = FastAPI(title="Inline", lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(pages_router)
app.include_router(api_router)
