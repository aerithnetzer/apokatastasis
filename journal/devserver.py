from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import build

PUBLIC_DIR = Path("public")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    build.build_site()
    yield
    # Shutdown (optional cleanup)
    # nothing needed here

app = FastAPI(lifespan=lifespan)

app.mount(
    "/",
    StaticFiles(directory=PUBLIC_DIR, html=True),
    name="static",
)
