from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from contextlib import asynccontextmanager
from pathlib import Path
import threading
import build
from watch import watch

PUBLIC_DIR = Path("public")

@asynccontextmanager
async def lifespan(app: FastAPI):
    build.build_site()

    t = threading.Thread(target=watch, daemon=True)
    t.start()

    yield

app = FastAPI(lifespan=lifespan)

app.mount(
    "/",
    StaticFiles(directory=PUBLIC_DIR, html=True),
    name="static",
)
