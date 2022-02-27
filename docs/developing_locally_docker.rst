Local Development
==========================================

.. index:: docker, local

The steps below will get you up and running with a local development environment.
All of these commands assume you are in the root of your generated project.

.. note::

    If you're new to Docker, please be aware that some resources are cached system-wide
    and might reappear if you generate a project multiple times with the same name (e.g.
    `this issue with Postgres <https://cookiecutter-django.readthedocs.io/en/latest/troubleshooting.html#docker-postgres-auth-failed>`_).


Prerequisites
-------------

* Docker; if you don't have it yet, follow the `installation instructions`_;
* Docker Compose; refer to the official documentation for the `installation guide`_.
* Pre-commit; refer to the official documentation for the `pre-commit`_.

.. _`installation instructions`: https://docs.docker.com/install/#supported-platforms
.. _`installation guide`: https://docs.docker.com/compose/install/
.. _`pre-commit`: https://pre-commit.com/#install

Build the Stack
---------------

Register SSH_PRIVATE_KEY
~~~~~~~~~~~~~~~~~~~~~~~~~

We use git+ssh to install CCXT Pro (private repository). If you do not have subscription to `CCXT Pro <https://ccxt.pro/>`_, please subscribe and make sure that your public key is registered to your subscribed Github Account.
After that, please do the following before you build anything::

    $ export SSH_PRIVATE_KEY=$(cat ~/.ssh/id_rsa)  // id_rsa should be the Github SSH key

You may add this to your ``bashrc`` or ``zshrc`` so that you do not have to repeat whenever you try to build images.

Add LD local domain name to /etc/hosts
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Please add domain name in /etc/hosts like below::

    /etc/hosts
    127.0.0.1  local.ld-investment.ai


Build docker images
~~~~~~~~~~~~~~~~~~~~~~~~

This can take a while, especially the first time you run this particular command on your development system::

    $ docker-compose -f platform.local.yml build

Generally, if you want to emulate production environment use ``platform.prod.yml`` instead. And this is true for any other actions you might need to perform: whenever a switch is required, just do it!

Before doing any git commit, `pre-commit`_ should be installed globally on your local machine, and then::

    $ git init
    $ pre-commit install

Failing to do so will result with a bunch of CI and Linter errors that can be avoided with pre-commit.


Modify docker image
~~~~~~~~~~~~~~~~~~~~~~~~
If you modified source code and want to build image again, you need to stop containers that are running, remove images and caches.
For example, if you want to build image for ``ld_platform_local_collector`` again, ::

    $ docker stop collector_producer            # stop container
    $ docker rm collector_producer              # remove container
    $ docker rmi ld_platform_local_collector    # remove image
    $ docker system prune                       # remove cache
    $ docker-compose -f platform.local.yml build         # build again

Alternatively, you can build with no cache option as well ::

    $ docker-compose -f platform.local.yml build --no-cache

Run the Stack
-------------

This brings up both Django and PostgreSQL. The first time it is run it might take a while to get started, but subsequent runs will occur quickly.

Open a terminal at the project root and run the following for local development::

    $ docker-compose -f platform.local.yml up

You can also set the environment variable ``COMPOSE_FILE`` pointing to ``platform.local.yml`` like this::

    $ export COMPOSE_FILE=platform.local.yml

And then run::

    $ docker-compose up

To run in a detached (background) mode, just::

    $ docker-compose up -d


Check LD Platform and Django Admin
------------------------------------

Navigate to http://local.ld-investment.ai for LD Platform Landing page and http://local.ld-investment.ai/admin for Django Admin page.

- Django Admin ID: `admin`
- Django Admin Password: `333`


Execute Management Commands
---------------------------

As with any shell command that we wish to run in our container, this is done using the ``docker-compose -f ld_platform.local.yml run --rm`` command: ::

    $ docker-compose -f platform.local.yml run --rm django python manage.py migrate
    $ docker-compose -f platform.local.yml run --rm django python manage.py createsuperuser


Here, ``django`` is the target service we are executing the commands against.

You can alternatively enter into container and exectue commands as well: ::

    $ docker execute -it django bash
    $ python manage.py migrate


(Optionally) Designate your Docker Development Server IP
--------------------------------------------------------

When ``DEBUG`` is set to ``True``, the host is validated against ``['localhost', '127.0.0.1', '[::1]']``. This is adequate when running a ``virtualenv``. For Docker, in the ``config.settings.local``, add your host development server IP to ``INTERNAL_IPS`` or ``ALLOWED_HOSTS`` if the variable exists.


.. _envs:


(TODO) Check Swagger while developing API
--------------------------------------------------------
We use swagger & redoc as a tool for designing, documenting and collaborating on L&D Platform APIs. This is only applied to local development setting.

(TODO) Navigate to http://127.0.0.1:8000/swagger for Swagger page.

Please refer `django-yasg`_ for more info.

.. _`django-yasg`: https://drf-yasg.readthedocs.io/en/stable/readme.html


Configuring the Environment
---------------------------

This is the excerpt from your project's ``platform.local.yml``: ::

  # ...

  postgres:
    build:
      context: .
      dockerfile: ./compose/production/postgres/Dockerfile
    volumes:
      - local_postgres_data:/var/lib/postgresql/data
      - local_postgres_data_backups:/backups
    env_file:
      - ./.envs/.local/.postgres

  # ...

The most important thing for us here now is ``env_file`` section enlisting ``./.envs/.local/.postgres``. Generally, the stack's behavior is governed by a number of environment variables (`env(s)`, for short) residing in ``envs/``, for instance, this is what we generate for you: ::

    .envs
    ├── .local
    │   ├── .django
    │   └── .postgres
    └── .production
        ├── .django
        └── .postgres

By convention, for any service ``sI`` in environment ``e`` (you know ``someenv`` is an environment when there is a ``someenv.yml`` file in the project root), given ``sI`` requires configuration, a ``.envs/.e/.sI`` `service configuration` file exists.

Consider the aforementioned ``.envs/.local/.postgres``: ::

    # PostgreSQL
    # ------------------------------------------------------------------------------
    POSTGRES_HOST=postgres
    POSTGRES_DB=<your project slug>
    POSTGRES_USER=XgOWtQtJecsAbaIyslwGvFvPawftNaqO
    POSTGRES_PASSWORD=jSljDz4whHuwO3aJIgVBrqEml5Ycbghorep4uVJ4xjDYQu0LfuTZdctj7y0YcCLu

The three envs we are presented with here are ``POSTGRES_DB``, ``POSTGRES_USER``, and ``POSTGRES_PASSWORD`` (by the way, their values have also been generated for you). You might have figured out already where these definitions will end up; it's all the same with ``django`` service container envs.

One final touch: should you ever need to merge ``.envs/.production/*`` in a single ``.env`` run the ``merge_production_dotenvs_in_dotenv.py``: ::

    $ python merge_production_dotenvs_in_dotenv.py

The ``.env`` file will then be created, with all your production envs residing beside each other.


Tips & Tricks
-------------

Activate a Docker Machine
~~~~~~~~~~~~~~~~~~~~~~~~~

This tells our computer that all future commands are specifically for the dev1 machine. Using the ``eval`` command we can switch machines as needed.::

    $ eval "$(docker-machine env dev1)"

Debugging
~~~~~~~~~

ipdb
"""""

If you are using the following within your code to debug: ::

    import ipdb; ipdb.set_trace()

Then you may need to run the following for it to work as desired: ::

    $ docker-compose -f platform.local.yml run --rm --service-ports django


django-debug-toolbar
""""""""""""""""""""

In order for ``django-debug-toolbar`` to work designate your Docker Machine IP with ``INTERNAL_IPS`` in ``local.py``.


docker
""""""

The ``container_name`` from the yml file can be used to check on containers with docker commands, for example: ::

    $ docker logs worker
    $ docker top worker


Mailhog
~~~~~~~

When developing locally you can go with MailHog_ for email testing provided ``use_mailhog`` was set to ``y`` on setup. To proceed,

#. make sure ``mailhog`` container is up and running;

#. open up ``http://127.0.0.1:8025``.

.. _Mailhog: https://github.com/mailhog/MailHog/

.. _`CeleryTasks`:

Celery tasks in local development
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When not using docker Celery tasks are set to run in Eager mode, so that a full stack is not needed. When using docker the task scheduler will be used by default.

If you need tasks to be executed on the main thread during development set CELERY_TASK_ALWAYS_EAGER = True in config/settings/local.py.

Possible uses could be for testing, or ease of profiling with DJDT.

.. _`CeleryFlower`:

Celery Flower
~~~~~~~~~~~~~

`Flower`_ is a "real-time monitor and web admin for Celery distributed task queue".

Prerequisites:

* ``use_docker`` was set to ``y`` on project initialization;
* ``use_celery`` was set to ``y`` on project initialization.

By default, it's enabled both in local and production environments (``platform.local.yml`` and ``ld_platform.prod.yml`` Docker Compose configs, respectively) through a ``flower`` service. For added security, ``flower`` requires its clients to provide authentication credentials specified as the corresponding environments' ``.envs/.local/.django`` and ``.envs/.production/.django`` ``CELERY_FLOWER_USER`` and ``CELERY_FLOWER_PASSWORD`` environment variables. Check out ``localhost:5555`` and see for yourself.

.. _`Flower`: https://github.com/mher/flower

config/settings/local.py
~~~~~~~~~~~~~~~~~~~~~~~~

You should allow the new hostname. ::

  ALLOWED_HOSTS = ["localhost", "0.0.0.0", "127.0.0.1", "my-dev-env.local"]

Rebuild your ``docker`` application. ::

  $ docker-compose -f platform.local.yml up -d --build

Go to your browser and type in your URL bar ``https://my-dev-env.local``

See `https with nginx`_ for more information on this configuration.

  .. _`https with nginx`: https://codewithhugo.com/docker-compose-local-https/

.gitignore
~~~~~~~~~~

Add ``certs/*`` to the ``.gitignore`` file. This allows the folder to be included in the repo but its contents to be ignored.

*This configuration is for local development environments only. Do not use this for production since you might expose your local* ``rootCA-key.pem``.
