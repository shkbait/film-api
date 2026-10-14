from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.openapi.utils import get_openapi
from src.api.repository import security

from src.api.router import main_router

app=FastAPI()
app.include_router(main_router)
app.mount("/static", StaticFiles(directory="uploads"),name="static")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500","http://localhost:5500"]
)
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)

# python -m uvicorn src.main:app --reload
