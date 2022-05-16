from os import environ
from dotenv import load_dotenv, find_dotenv
import uvicorn
from src.config.logging import LOGGING_CONFIG
from src import app


load_dotenv(find_dotenv())

app = app

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=environ["HOST"] if "HOST" in environ else "0.0.0.0",  # nosec
        port=int(environ["PORT"]) if "PORT" in environ else 5000,
        reload=bool(environ.get("DEBUG_MODE") == "True"),
        log_config=LOGGING_CONFIG,
    )
