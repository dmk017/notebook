FROM python:3.11-slim-bullseye
WORKDIR /auth_code_consumer
RUN pip install poetry==1.6.1
COPY . /auth_code_consumer
RUN poetry install
EXPOSE 5009
CMD [ "poetry", "run", "dev"]