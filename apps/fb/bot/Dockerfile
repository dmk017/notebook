FROM python:3.11-slim-bullseye
WORKDIR /fortuna_bot
RUN pip install poetry==1.6.1
COPY . /fortuna_bot
RUN poetry install
EXPOSE 5008
CMD [ "poetry", "run", "dev"]