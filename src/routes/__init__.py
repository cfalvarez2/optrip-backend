from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


index = APIRouter()

templates = Jinja2Templates(directory="src/templates")


@index.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {'request': request, 'version': "0.1.1"}
    )
