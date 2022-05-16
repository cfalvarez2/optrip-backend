# FastAPI Template for Tucar
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://GitHub.com/Naereen/StrapDown.js/graphs/commit-activity) [![Linux](https://svgshare.com/i/Zhy.svg)](https://svgshare.com/i/Zhy.svg) [![PyPi license](https://badgen.net/pypi/license/pip/)](https://pypi.com/project/pip/)

## Main Env Variables
```
DB_USERNAME=<DB username if it needs one>
DB_PASSWORD=<DB password if it needs one>
DB_NAME=<name of database>
DB_HOST=<name or ip of database host>
DB_PORT=<port of database, default 27017>
DEBUG_MODE=<If debug or not>
LOG_LEVEL=<Log levels, mainly DEBUG or INFO>
PY_ENV=<production or development, default development>
```
Place the `.env` file in the root of this directory.

## Run docker on local machine
1. Run `docker-compose up`
2. Enjoy!

## Recomendations

- Read Pydantic, Beanie, FastAPI and Motor.  
- For any change, please request va pull request.  
- Install Mongo Compass.  
