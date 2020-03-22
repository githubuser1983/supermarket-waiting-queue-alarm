FROM python:3.8.1-slim

ENV PYTHONUNBUFFERED 1

# apt update
RUN apt-get update
RUN apt-get install -y apt-utils

# to get rid of ERROR: debconf: unable to initialize frontend: Dialog
RUN echo 'debconf debconf/frontend select Noninteractive' | debconf-set-selections

# build base debian stuff
RUN apt-get install -y \
  gcc \
  g++

# apt upgrade
RUN apt-get -y dist-upgrade

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # postgres client psql for python manage.py dbshell
  && apt-get install -y postgresql-client \
  # curl to be able to install poetry
  && apt-get install -y curl \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# just to make sure we're on current pip
RUN pip install -U pip

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
RUN mkdir /etc/bash_completion.d
RUN /root/.poetry/bin/poetry completions bash > /etc/bash_completion.d/poetry.bash-completion

# Project Initialization
COPY poetry.lock pyproject.toml /app/
WORKDIR /app
RUN /root/.poetry/bin/poetry config virtualenvs.create false \
    && /root/.poetry/bin/poetry install --no-interaction --no-ansi --no-root


COPY ./compose/local/django/entrypoint /entrypoint
RUN sed -i 's/\r//' /entrypoint
RUN chmod +x /entrypoint

# notebook stuff
RUN mkdir /root/.jupyter
COPY ./compose/local/django/jupyter_notebook_config.py /root/.jupyter
COPY ./compose/local/django/start_notebook.sh /start_notebook.sh
RUN sed -i 's/\r//' /start_notebook.sh
RUN chmod +x /start_notebook.sh

COPY ./compose/local/django/start /start
RUN sed -i 's/\r//' /start
RUN chmod +x /start

COPY ./compose/local/django/start_regular /start_regular
RUN sed -i 's/\r//' /start_regular
RUN chmod +x /start_regular

COPY ./compose/local/django/celery/worker/start /start-celeryworker
RUN sed -i 's/\r//' /start-celeryworker
RUN chmod +x /start-celeryworker

COPY ./compose/local/django/celery/beat/start /start-celerybeat
RUN sed -i 's/\r//' /start-celerybeat
RUN chmod +x /start-celerybeat

COPY ./compose/local/django/celery/flower/start /start-flower
RUN sed -i 's/\r//' /start-flower
RUN chmod +x /start-flower

WORKDIR /app

ENTRYPOINT ["/entrypoint"]
