from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from os import environ


VALUES = {
    'user': environ.get("DB_USERNAME"),
    'pass': environ.get("DB_PASSWORD"),
    'name': environ.get("DB_NAME"),
    'host': environ.get("DB_HOST") if environ.get("DB_HOST") else "localhost",
    'port': environ.get("DB_PORT") if environ.get("DB_PORT") else "27017",
}

MONGO_ODM = {
    'development': {
        'url': "mongodb://mongo",
        'tls': False,
    },
    'production': {
        'url': (
            f"mongodb+srv://{VALUES['user']}:{VALUES['pass']}"
            f"@{VALUES['host']}:{VALUES['port']}"
        ),
        'tls': True,
    },
}

MODELS = [
    "src.models.complex_test.ComplexTest",
    "src.models.Company"
    "src.models.City"
    "src.models.RouteLeg"
    "src.models.Route",
]


async def init_db() -> AsyncIOMotorClient:
    parameters = MONGO_ODM["development"]
    if environ.get("PY_ENV") == "production":
        parameters = MONGO_ODM["production"]
    client = AsyncIOMotorClient(parameters["url"], tls=parameters["tls"])
    await init_beanie(
        database=client[environ.get("DB_NAME")],
        document_models=MODELS
    )
    return client[VALUES["name"]]
