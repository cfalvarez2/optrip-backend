FROM python:3.10-slim-buster
RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && apt-get purge -y ca-certificates curl
CMD ["python", "app_turbus.py"]
