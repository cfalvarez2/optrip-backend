from urllib import response
from fastapi import APIRouter, Request, status, Body
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

from typing import List, Union
from bson import json_util
import json

from ..models import Company, City, RouteLeg, Route
from ..config.database import init_db

index = APIRouter()

templates = Jinja2Templates(directory="src/templates")

@index.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {'request': request, 'version': "0.1.1"}
    )

@index.get("/route-legs", response_description="List all Route Legs", response_model=List[RouteLeg])
async def list_route_legs(request: Request):
    db = await init_db()
    route_legs = await db["routeleg"].find(dict(request.query_params)).to_list(1000) # .limit
    return json.loads(json_util.dumps(route_legs))

@index.post("/route-legs", response_description="Create a route leg", response_model=RouteLeg)
async def create_route_leg(route_leg: RouteLeg = Body(...)):
    db = await init_db()
    route_leg = jsonable_encoder(route_leg)
    new_route_leg = await db["routeleg"].insert_one(route_leg)
    created_route_leg = await db["routeleg"].find_one({"_id": new_route_leg.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_route_leg)
