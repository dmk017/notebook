# Dev mode

Для локальной разработки надо запустить контейнер прокси и фронта:

```
docker compose -f docker-compose.dev.yml up -d --build --force-recreate
```

Запустить бекенд (надо перенести в папку fb тк это облегчит деплой)

Добавить контейнер с прокси и бекендом в одну сеть

```
docker network create dev-proxy-net
docker network connect dev-proxy-net <oauth-proxy-container-id>
docker network connect dev-proxy-net <fb-api-id>
```

Проверить можно командой
```
docker network inspect dev-proxy-net
```