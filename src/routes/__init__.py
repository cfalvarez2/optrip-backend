from urllib import response
from fastapi import APIRouter, Request, status, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
import requests

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


### Routes ###

@index.get("/routes", response_description="List all routes", response_model=List[Route])
async def list_routes(request: Request):
    db = await init_db()
    routes = await db["route"].find(dict(request.query_params)).to_list(1000)
    return json.loads(json_util.dumps(routes))

@index.post("/routes", response_description="Create a route", response_model=Route)
async def create_route(route: Route = Body(...)):
    db = await init_db()
    route = jsonable_encoder(route)
    new_route = await db["route"].insert_one(route)
    created_route = await db["route"].find_one({"_id": new_route.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_route)

@index.get("/routes/{id}", response_description="Get a single route", response_model=Route)
async def show_route(id: str):
    db = await init_db()
    if (route := await db["route"].find_one({"_id": id})) is not None:
        return route
    raise HTTPException(status_code=404, detail=f"Route {id} not found")

@index.put("/routes/{id}", response_description="Update a route", response_model=Route)
async def update_route(id: str, route: Route = Body(...)):
    route = {k: v for k, v in route.dict().items() if v is not None}
    if len(route) >= 1:
        db = await init_db()
        update_result = await db["route"].update_one({"_id": id}, {"$set": route})
        if update_result.modified_count == 1:
            if (
                updated_route := await db["route"].find_one({"_id": id})
            ) is not None:
                return updated_route
    if (existing_route := await db["route"].find_one({"_id": id})) is not None:
        return existing_route
    raise HTTPException(status_code=404, detail=f"Route {id} not found")

@index.delete("/routes/{id}", response_description="Delete a route")
async def delete_route(id: str):
    db = await init_db()
    delete_result = await db["route"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Route {id} not found")


### Route Legs ###

@index.get("/route-legs", response_description="List all route legs", response_model=List[RouteLeg])
async def list_route_legs(request: Request):
    db = await init_db()
    route_legs = await db["routeleg"].find(dict(request.query_params)).to_list(1000)
    return json.loads(json_util.dumps(route_legs))

@index.post("/route-legs", response_description="Create a route leg", response_model=RouteLeg)
async def create_route_leg(route_leg: RouteLeg = Body(...)):
    db = await init_db()
    route_leg = jsonable_encoder(route_leg)
    new_route_leg = await db["routeleg"].insert_one(route_leg)
    created_route_leg = await db["routeleg"].find_one({"_id": new_route_leg.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_route_leg)

@index.get("/route-legs/{id}", response_description="Get a single route leg", response_model=RouteLeg)
async def show_route_leg(id: str):
    db = await init_db()
    if (route_leg := await db["routeleg"].find_one({"_id": id})) is not None:
        return route_leg
    raise HTTPException(status_code=404, detail=f"Route leg {id} not found")

@index.put("/route-legs/{id}", response_description="Update a route leg", response_model=RouteLeg)
async def update_route_leg(id: str, route_leg: RouteLeg = Body(...)):
    route_leg = {k: v for k, v in route_leg.dict().items() if v is not None}
    if len(route_leg) >= 1:
        db = await init_db()
        update_result = await db["routeleg"].update_one({"_id": id}, {"$set": route_leg})
        if update_result.modified_count == 1:
            if (
                updated_route_leg := await db["routeleg"].find_one({"_id": id})
            ) is not None:
                return updated_route_leg
    if (existing_route_leg := await db["routeleg"].find_one({"_id": id})) is not None:
        return existing_route_leg
    raise HTTPException(status_code=404, detail=f"Route leg {id} not found")

@index.delete("/route-legs/{id}", response_description="Delete a route leg")
async def delete_route_leg(id: str):
    db = await init_db()
    delete_result = await db["routeleg"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Route leg {id} not found")


### Cities ###

@index.get("/cities", response_description="List all cities", response_model=List[City])
async def list_cities(request: Request):
    db = await init_db()
    cities = await db["city"].find(dict(request.query_params)).to_list(1000)
    return json.loads(json_util.dumps(cities))

@index.post("/cities", response_description="Create a city", response_model=City)
async def create_city(city: City = Body(...)):
    db = await init_db()
    city = jsonable_encoder(city)
    new_city = await db["city"].insert_one(city)
    created_city = await db["city"].find_one({"_id": new_city.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_city)

@index.get("/cities/{id}", response_description="Get a single city", response_model=City)
async def show_city(id: str):
    db = await init_db()
    if (city := await db["city"].find_one({"_id": id})) is not None:
        return city
    raise HTTPException(status_code=404, detail=f"City {id} not found")

@index.put("/cities/{id}", response_description="Update a city", response_model=City)
async def update_city(id: str, city: City = Body(...)):
    city = {k: v for k, v in city.dict().items() if v is not None}
    if len(city) >= 1:
        db = await init_db()
        update_result = await db["city"].update_one({"_id": id}, {"$set": city})
        if update_result.modified_count == 1:
            if (
                updated_city := await db["city"].find_one({"_id": id})
            ) is not None:
                return updated_city
    if (existing_city := await db["city"].find_one({"_id": id})) is not None:
        return existing_city
    raise HTTPException(status_code=404, detail=f"City {id} not found")

@index.delete("/cities/{id}", response_description="Delete a city")
async def delete_city(id: str):
    db = await init_db()
    delete_result = await db["city"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"City {id} not found")


### Companies ####

@index.get("/companies", response_description="List all companies", response_model=List[Company])
async def list_companies(request: Request):
    db = await init_db()
    companies = await db["company"].find(dict(request.query_params)).to_list(1000)
    return json.loads(json_util.dumps(companies))

@index.post("/companies", response_description="Create a company", response_model=Company)
async def create_company(company: Company = Body(...)):
    db = await init_db()
    company = jsonable_encoder(company)
    new_company = await db["company"].insert_one(company)
    created_company = await db["company"].find_one({"_id": new_company.inserted_id})
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_company)

@index.get("/companies/{id}", response_description="Get a single company", response_model=Company)
async def show_company(id: str):
    db = await init_db()
    if (company := await db["company"].find_one({"_id": id})) is not None:
        return company
    raise HTTPException(status_code=404, detail=f"Company {id} not found")

@index.put("/companies/{id}", response_description="Update a company", response_model=Company)
async def update_company(id: str, company: Company = Body(...)):
    company = {k: v for k, v in company.dict().items() if v is not None}
    if len(company) >= 1:
        db = await init_db()
        update_result = await db["company"].update_one({"_id": id}, {"$set": company})
        if update_result.modified_count == 1:
            if (
                updated_company := await db["company"].find_one({"_id": id})
            ) is not None:
                return updated_company
    if (existing_company := await db["company"].find_one({"_id": id})) is not None:
        return existing_company
    raise HTTPException(status_code=404, detail=f"Company {id} not found")

@index.delete("/companies/{id}", response_description="Delete a company")
async def delete_company(id: str):
    db = await init_db()
    delete_result = await db["company"].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Company {id} not found")


### Flights ###

@index.post("/flights", response_description="List all flights")
async def list_flights(request: Request):
    data_json = await request.json()
    get_flights_response = requests.get(
        "http://scraper:3000/flights", 
        headers = {'content-type': 'application/json'},
        data=json.dumps(data_json))
    print(get_flights_response)
    return json.loads(get_flights_response.content.decode('utf-8'))
