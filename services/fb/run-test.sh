if [ "$(docker ps -aq -f name=fb-api-test)" ]; then
    docker rm fb-api-test
else
    echo "Контейнер fb-api-test не существует"
fi

docker build -t fb-api-test -f Dockerfile.test .

docker run --network fortuna_mongo-db-net --name fb-api-test fb-api-test