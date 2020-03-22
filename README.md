
# supermarket-waiting-queue-alarm

Due to the Covid-19 virus it is expected that supermarkets will allow to enter only a handful of people at a given time period. This means there will be waiting queues in front of the supermarket. To help reduce the spreading of the virus, people on the waiting queue could use a web-app to warn others of the queue by simply pressing a button. Others will see on the web-app how many warnings are for this supermarket and might decide to go to another supermarket or wait at home. The principle is already implemented in anti-traffic-jam apps with user generated content. The app does not work yet, but the user interface (html) does and is kept simple.
If someone with knowledge in JQuery/Python can improve this, that would be great. Also if you do not want to code, but have the possibility to host the app for your city/community, that would also be great.

I will make the start by hosting this incomplete app at:
http://www.orges-leka.de/limburg.html

> WirVScoronaHackathon 2020 - an application implemented in django - using docker &amp; postgres

## requirements

`poetry`, `docker` & `docker-compose` are installed and functional

linux / macos: I pretend you know, what you are doing.

Windows >= Windows10 Professional

for using `redis` on windows you need a `wsl` environment.

## installation & startup of development server

clone the repo

cd into to root-projetcs-dir

```shell
# install the environment
poetry install

# build the docker-containers
docker-compose build

# makemigrations
docker-compose run django /app/manage.py makemigrations
docker-compose run django /app/manage.py migrate

# create a superuser
docker-compose run django /app/manage.py createsuperuser

# start the containers
docker-compose up
```

to have the hostname `supermarket` available (set in allowed_hosts in settings,
localhost is not allowed), edit `/etc/hosts` (linux) or
`c:\Windows\System32\drivers\etc\hosts` and add an entry for 127.0.0.1. After
setting this up, you can access the running django-app's docker-instance via
`supermarket:8000` in your browser

```/etc/hosts
# local supermarket project
127.0.0.1 supermarket
```

### start working on your own development/feature branch

`git flow feature start <your featurename>`

## erm-graph with grahpviz

to create an erm-graph install `grahpviz` on your system and run these two
management commands `./manage.py graph_models -a > erm/erm_graph.dot` &
`./manage.py graph_models -a -g -o erm_graph.png`

## running celery (with redis)

on windows:

- install gevent binaries from `https://www.lfd.uci.edu/~gohlke/pythonlibs/#gevent`
- install `redis` on wsl
- check if redis is running with `redis-cli ping` (restart with: `sudo service redis-server restart`)
- run `celery -A config.celery worker -l info -P gevent -E`
- alternative for recurring tasks: `celery -A config beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler`
- analytics with flower `celery flower -A config --address=127.0.0.1 --port=5555`

start all celery services at once with docker:
`docker-compose up -d celeryworker celerybeat flower`

## Test coverage

To run the tests, check your test coverage, and generate an HTML coverage report::

```shell
    coverage run -m pytest
    coverage html
    open htmlcov/index.html
```

Running tests with py.test

```shell
  pytest  # BUG: CELERY_BROKER_URL is not available, Dominik 20-03-20
```
