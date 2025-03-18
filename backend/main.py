from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import os
from api import router  

app = FastAPI()

static_dir = "static"
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
    print(f"[INFO] Created static directory: {static_dir}")

app.mount("/static", StaticFiles(directory=static_dir), name="static")
app.include_router(router)