FROM python:3.11-slim-bullseye
WORKDIR /app

COPY . /app

RUN pip install poetry==1.6.1
RUN poetry install --sync
RUN apt-get update && apt-get install -y libmagic-dev

EXPOSE 5002
CMD [ "poetry", "run", "dev"]