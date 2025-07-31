# df -h
# docker builder prune

APP_MODE=DEV docker compose up -d --build --force-recreate
APP_MODE=PROD docker compose up -d --build --force-recreate