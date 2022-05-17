FROM python:3.10-alpine

RUN apk update && apk --no-cache add \
    gcc \
    libc-dev \
    musl-dev \
    openblas \
    gfortran \
    build-base \
    libffi-dev \
    curl

RUN curl -sSL https://install.python-poetry.org | python -
# Adding poetry to PATH
ENV PATH /root/.local/bin:$PATH

# Create app directory
RUN mkdir /app
WORKDIR /app

# Copy needed files
COPY ./pyproject.toml .
COPY ./poetry.lock .

# Install dependencies
RUN poetry install

# Copy rest of files
COPY . .

# Expose and start server
EXPOSE 5000
CMD ["poetry", "run", "python", "main.py"]
