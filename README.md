

# LostАndFoundSite

## Docker Installation

Build and run the project:

    docker compose up --build

To run Django commands like migrations and shell or to enter the
container bash do:

    docker compose run --rm app bash
    docker compose run --rm app manage.py createsuperuser
    docker compose run --rm app manage.py migrate
    docker compose run --rm app manage.py shell

To stop containers run:

    docker compose down

To update a container after adding a new requirement for example:

    docker compose build

## Running the project

### Docker

Create super user:

    docker compose run --rm app manage.py createsuperuser

Make sure you have the containers running:

    docker compose up

Access [localhost:8000/LostАndFoundSite-admin/](http://localhost:8000/LostАndFoundSite-admin/).

## Configuration / Environment Variables

<!-- [[[cog
import cog
from LostAndFoundSite.config import Config
mdown = Config.generate_markdown()
cog.out('\n'.join(mdown.split('\n')[1:]))
]]] -->

* **DEBUG**
  * type: `bool`
  * default: `False`
* **ALLOWED_HOSTS**
  * description: Hosts allowed to serve the site https://docs.djangoproject.com/en/5.2/ref/settings/#allowed-hosts
  * type: `list[str]`
  * default: `['*']`
* **DATABASE_URL**
  * description: A string with the database URL as defined in https://github.com/jazzband/dj-database-url#url-schema
  * type: `str`
  * default: `sqlite:///./sqlite3.db`
* **DJANGO_ENV**
  * description: Toggle deployment settings for local development or production
  * type: `Literal['development', 'dev', 'production']`
  * default: `production`
* **LOG_LEVEL**
  * description: Python logging level
  * type: `Literal['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']`
  * default: `INFO`
* **SECRET_KEY** _REQUIRED_
  * description: A long random string you keep secret https://docs.djangoproject.com/en/5.2/ref/settings/#secret-key
  * type: `str`
* **ENVIRONMENT**
  * description: Name of deployed environment (e.g. 'staging', 'production')
  * type: `str`
  * default: `development`
* **BASIC_AUTH_CREDENTIALS**
  * description: Basic Auth credentials for the site in the format 'username:password'
  * type: `str`
  * default: ``
* **SENTRY_DSN**
  * description: Sentry DSN to enable error logging
  * type: `str`
  * default: ``
* **SENTRY_TRACES_SAMPLE_RATE**
  * description: Sentry trace sample rate https://docs.sentry.io/product/sentry-basics/concepts/tracing/trace-view/
  * type: `float`
  * default: `0.25`
<!-- [[[end]]] -->

## Makefile commands

<!-- [[[cog
import cog
import subprocess
cog.out(
    "```shell\n" +
    subprocess.check_output(["make", "help"]).decode() +
    "```"
)
]]] -->
```shell
Available make commands:

README.md                 Update dynamic blocks in README.md
fix                       Fix linting errors
fmt                       Format Python code
lint                      Lint Python code
test                      Run tests
upgrade-requirements      Upgrade all dependencies in uv.lock
```
<!-- [[[end]]] -->



КАК ПОЛУЧИТЬ СЕРТИФИКАТЫ

Вы исправили синтаксическую ошибку, и теперь Nginx сталкивается со следующей проблемой: он не может найти SSL-сертификаты.

Ошибка `cannot load certificate ... No such file or directory` означает, что Nginx пытается запуститься с конфигурацией для HTTPS (порт 443), но файлы сертификатов, которые вы указали, еще не существуют.

Это классическая проблема "курицы и яйца":
1.  Чтобы Nginx запустился, ему нужны SSL-сертификаты.
2.  Чтобы Certbot (сервис, который получает сертификаты) сработал, ему нужен запущенный Nginx для прохождения проверки.

**Решение:**

Вам нужно временно закомментировать в `nginx.conf` всю секцию, отвечающую за HTTPS, чтобы Nginx мог запуститься только на порту 80. Это позволит Certbot'у получить сертификаты. После этого вы вернете конфигурацию обратно.

**Шаг 1: Измените `nginx.conf`**

Замените содержимое вашего файла `nginx/nginx.conf` на эту временную конфигурацию. Здесь закомментирован весь блок `server` для порта 443.

```nginx
upstream django_app {
    server web:8000;
}

server {
    listen 80;
    listen [::]:80;
    server_name things.ifknow.ru;

    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

# server {
#     listen 443 ssl;
#     listen [::]:443;
#     server_name things.ifknow.ru;
#
#     ssl_certificate /etc/letsencrypt/live/things.ifknow.ru/fullchain.pem;
#     ssl_certificate_key /etc/letsencrypt/live/things.ifknow.ru/privkey.pem;
#
#     location /static/ {
#         alias /app/staticfiles/;
#     }
#
#     location / {
#         proxy_pass http://django_app;
#         proxy_set_header Host $host;
#         proxy_set_header X-Real-IP $remote_addr;
#         proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#         proxy_set_header X-Forwarded-Proto $scheme;
#     }
# }
```

**Шаг 2: Перезапустите Nginx**

```bash
docker-compose up -d --force-recreate nginx
```

**Шаг 3: Получите сертификаты**

Теперь, когда Nginx работает на порту 80, запустите Certbot. (Эта команда зависит от того, как у вас настроен сервис `certbot` в `docker-compose.yaml`, но обычно она выглядит так):

```bash
docker-compose run --rm certbot certonly --webroot --webroot-path /var/www/certbot --email ВАШ_EMAIL@example.com -d things.ifknow.ru --agree-tos --no-eff-email -v
```
*Замените `ВАШ_EMAIL@example.com` на ваш реальный email.*

**Шаг 4: Верните конфигурацию Nginx**

После успешного получения сертификатов верните файл `nginx/nginx.conf` к исходному состоянию (с раскомментированным блоком для порта 443).

**Шаг 5: Финальный перезапуск**

Снова перезапустите все сервисы, чтобы Nginx подхватил новую конфигурацию с SSL.

```bash
docker-compose up -d --force-recreate
```