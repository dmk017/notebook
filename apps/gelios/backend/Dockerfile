FROM python:3.11-slim-bullseye

# create workdir and copy files
WORKDIR /gelios
COPY . /gelios


# install dependencies
RUN pip install poetry==1.7.1
RUN poetry install --sync
RUN apt-get update && apt-get clean


# open port
EXPOSE 5002
CMD [ "poetry", "run", "dev"]