ARG PYTHON_VERSION=3.9-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local
ARG SSH_PRIVATE_KEY

# Install apt packages
RUN apt-get update && apt-get install --no-install-recommends -y \
  # dependencies for building Python packages
  build-essential \
  # psycopg2 dependencies
  libpq-dev \
  # git ssh
  ssh git

# Add credentials on build
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh
RUN ssh-keyscan github.com > /root/.ssh/known_hosts
RUN echo "${SSH_PRIVATE_KEY}" > /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa

# Requirements are installed here to ensure they will be cached.
COPY ./requirements/collector .

# Create Python Dependency
RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Remove SSH keys
RUN rm -rf /root/.ssh/

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV BUILD_ENV ${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

# Install required system dependencies
RUN apt-get update \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

# All absolute dir copies ignore workdir instruction. All relative dir copies are wrt to the workdir instruction
# copy python dependency wheels from python-build-stage
COPY --from=python-build-stage /usr/src/app/wheels  /wheels/

# use wheels to install python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
	&& rm -rf /wheels/

COPY ./compose/local/collector/rmq/producer/start /start-producer
RUN sed -i 's/\r$//g' /start-producer
RUN chmod +x /start-producer

COPY ./compose/local/collector/rmq/consumer/start /start-consumer
RUN sed -i 's/\r$//g' /start-consumer
RUN chmod +x /start-consumer

# copy application code to WORKDIR
COPY ./collector ${APP_HOME}
