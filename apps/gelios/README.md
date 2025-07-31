
# Для запуска проекта

Для локального запуска проекта необходимо:

-  перейти в файл `../../services/admin-api/docker-compose.dev.yml` и раскомментировать сеть `gelios-dev-net` (если она закомментирована)
-  выполнить команду `docker compose -f docker-compose.dev.yml up -d --build`