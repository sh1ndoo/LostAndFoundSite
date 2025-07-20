

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
