# Система сервисов FORTUNA

На сегодняшний день поддерживаются и развиваются следующие сервисы:
- *admin-panel* - сервис администрирования и мониторинга системы
- *FB* - (Fortuna Bank) сервис накопления и поиска неструктурированной информации
- *Gelios* - сервиc автоматизированного построения VPN цепочек
- *WiKii* - сервис хранения и обработки информации о КИИ
- *UDF* - (user digital fingerprint) сервис формирования ссылок для сбора цифрового отпечатка пользователя 

Планируется в разработку:
- *eCMS* - сервис определения версии CMS и автоматизированного проникновения 

## Структура проекта

1. `apps` - папка с Frontend'ами сервисов.

    В каждой папке может быть:
    - `web` - отображение в виде сайта
    - `telegram` - Telegram-bot сервиса

2. `services` - папка с Backend сервисами
3. `libs` - папка с общеиспользуемыми библиотеками

## OAuth

Доступ к сервисам можно получить только по токену сформированную в системе администратором. Токен является "паролем" для `OpenID Connect` сайта.

> При необходимости Администратор может повысить привелегии в системе или деактивировать токен пользователя

## Локальный запуск авторизации

Для локального запуска Вам требуется запустить трм сервиса:

1. Reverse-proxy `traefik`
2. Сервис авторизации `Keycloak`
3. Прокси сервис `oauth2-proxy`
4. Пример Web-сервиса `httpbin`

Переходим в корень проекта и выполняем команду:

```
docker-compose up -d
```
Сервисы будут доступны по доменным адресам **nameService**.localtest.me

Также информацию о подключенных сервисах и их доменные имена можно посмотреть  в графическом интерфейсе traefik по адресу http://localhost:9091

### настройка Keycloak
Переходим в [Keycloak](http://keycloak.localtest.me)

Вводим логин и пароль админа (По умолчанию admin admin)

За логин и пароль отвечают переменные Keycloak в doker-compose:
```
KEYCLOAK_ADMIN: admin
KEYCLOAK_ADMIN_PASSWORD: admin
```

<details> <summary>Cоздаем нового клиента (Create client) </summary>

переходим в `clients`

- Client type - OpenID Connect
- Client ID - oauth2-proxy (Должен совпадать с указанным в data/oauth-proxy/oauth2-proxy-keycloak.cfg)

нажимаем **next**

- Client authentication - 'on'
- authentication flow
	- Standard flow - должно быть выбрано
    - Direct access grants - отключить

нажимаем **next**
- Valid redirect URIs ставим * (то есть разрешаем любой адрес, что в prod недопустимо)

**сохраняем**
</details>
<details> <summary>Настраиваем client для взаимодействия с OAuth-proxy</summary>

Заходим в нашего клиента


в **Credentials** копируем *Client Secret* и в [конфиге OAuth-proxy](./data/oauth-proxy/oauth2-proxy-keycloak.cfg) меняем соответсвующее значение (client_secret) на наше

Далее переходим в `Client scopes`

нажимаем на <your client's id>-dedicated  в нашем примере (*oauth2-proxy-dedicated*)

**add mapper** -> **by configuration** -> **Audience**

- Name  - 'aud-mapper-<your client's id>' (aud-mapper-oauth2-proxy)
- Included Client Audience  - выбираем наш client's id из выпадающего списка
- Add to ID token - 'On'
- Add to access token - 'On'

**Сохраняем**
</details>

<details> <summary>Cоздаем роль (Realm roles) </summary>

Переходим в `Realm roles`

Нажимаем *Create role*

- Role name - вводим желаемое имя роли (В нашем случае - **test_role**, согласно параметру `allowed_roles`  в [конфиге OAuth-proxy](./data/oauth-proxy/oauth2-proxy-keycloak.cfg))

**Сохраняем**
</details>

<details> <summary>Cоздаем Пользователя (Users) (можно пропустить и делать следующий шаг для админа)</summary>

переходим в `Users`

нажимаем *add user*

- Usernmae - это login под которым в дальнейшем будете заходить
нажимаем *создать*
</details>
<details> <summary>Добавления роли пользователю</summary>

Переходим в `Users`

Выбираем нашего пользователя

**Role mapping** -> **Assign role**

Выбираем необходимую нам роль (*test_role*)
нажимаем *assign*
</details>

Теперь мы можем зайти и пройти авторизацию в наш сервис [httpbin](http://httpbin.localtest.me)

## Get Started

Для локальной разработки Вам требуется:

- Склонировать проект в рабочую директорию с помощью `git clone https://gitlab.com/billysmalldefend/fortuna.git`
- Скачать docker и docker compose
    - Для удобства работы можно скачать docker-desktop
- Для запуска frontend и backend сделаем следующее:
    - в корне проекта пишем команду `docker compose up fb-api -d`, тем самым создали контейнеры для backend
    - далее переходим в директорию с frontend `cd apps/fb/web`
    - запускаем docker контейнеры для frontend с помощью `docker compose -f docker-compose.dev.yml up -d`
    - через команду `docker ps` смотрим какие контейнеры у нас работают, должно быть запущено 4 контейнера: web-fb-web, quay.io/oauth2-proxy/oauth2-proxy:v7.6.0, fortuna-fb-api, mongo:latest
        - может быть такое, что контейнер web-fb-web не будет виден через команду `docker ps`, можно посмотреть логи(`docker compose -f docker-compose.dev.yml logs -f`), если в логах видим, что docker не знает что такое typescript, чтобы его увидеть нам нужно запустить frontend на хосте
            - переходим в терминал и пишем следующие команды
                - `yarn install`
                - `yarn dev`
            - после чего docker увидит локальные файлы, далее пересоберем проект(все действия еще раз) и все контейнеры должны быть видны
        - также возможен случай, что контейнер fortuna-fb-api-1 не будет виден через команду `docker ps`, для того чтобы это исправить сделаем следующее:
            - нам необходимо добавить backend и frontend в одну сеть, с помощью команды `docker network ls` посмотрим все сети, которые у нас есть
            - найдем сеть frontend'а (web_fb-web-net), с помощью команды `docker inspect <NETWORK_ID>` посмотрим какие контейнеры находятся в сети frontend'а, и увидим, что в сети frontend'a нет контейнера backend'a, добавим его
            - `docker ps` находим CONTAINER_ID backend'a и пишем команду `docker network connect <NETWORK_ID> <CONTAINER_ID>`
            - убедимся, что добавили контейнер backend'a в сеть frontend'a `docker inspect <NETWORK_ID>`
            - если все на месте, можем приступить к работе: frontend `127.0.0.1:3001`, backend `127.0.0.1:3001/docs`
