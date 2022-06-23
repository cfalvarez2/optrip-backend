FROM python:3.10-slim-buster
RUN mkdir /code
COPY . /code
WORKDIR /code
RUN pip install -r requirements.txt
CMD ["python", "app.py"]
