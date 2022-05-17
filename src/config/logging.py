from os import environ
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())


LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            '()': "uvicorn.logging.DefaultFormatter",
            'format': "%(levelprefix)s %(asctime)s :: %(message)s",
            'use_colors': True,
        },
        'access': {
            '()': "uvicorn.logging.AccessFormatter",
            'format': (
                "%(levelprefix)s %(asctime)s :: %(client_addr)s"
                "\"%(request_line)s\" %(status_code)s"
            ),
            'use_colors': True,
        },
    },
    'handlers': {
        'default': {
            'formatter': "default",
            'class': "logging.StreamHandler",
            'stream': "ext://sys.stderr",
        },
        'access': {
            'formatter': "access",
            'class': "logging.StreamHandler",
            'stream': "ext://sys.stdout",
        },
    },
    'loggers': {
        'uvicorn.error': {
            'level': "INFO",
            'handlers': ["default"],
            'propagate': False,
        },
        'uvicorn.access': {
            'level': (
                environ["LOG_LEVEL"] if "LOG_LEVEL" in environ else "INFO"
            ),
            'handlers': ["access"],
            'propagate': False,
        },
    },
}
