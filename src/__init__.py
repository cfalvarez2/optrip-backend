from os import environ
from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .config.database import init_db
from .router import router


load_dotenv(find_dotenv())

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="src/static"), name="static")


@app.on_event("startup")
async def startup_db_client() -> None:
    app.db = await init_db()
    print(f"Connection stablished to {environ.get('DB_NAME')}")


@app.on_event("shutdown")
async def shutdown_db_client() -> None:
    app.mongodb_client.close()

app.include_router(router, dependencies=[Depends(startup_db_client)])
