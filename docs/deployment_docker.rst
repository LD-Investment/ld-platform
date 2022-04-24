Deployment with Docker
======================

.. index:: deployment, docker, docker-compose, compose


Prerequisites
-------------

* Docker 17.05+.
* Docker Compose 1.17+


Understanding the Docker Compose Setup
--------------------------------------

Before you begin, check out the ``platform.prod.yml`` file in the root of this project. Keep note of how it provides configuration for the following services:

* ``django``: your application running behind ``Gunicorn``;
* ``postgres``: PostgreSQL database with the application's relational data;
* ``redis``: Redis instance for caching;

Provided you have opted for Celery (via setting ``use_celery`` to ``y``) there are three more services:

* ``celeryworker`` running a Celery worker process;
* ``celerybeat`` running a Celery beat process;
* ``flower`` running Flower_.

The ``flower`` service is served by Traefik over HTTPS, through the port ``5555``. For more information about Flower and its login credentials, check out :ref:`CeleryFlower` instructions for local environment.

.. _`Flower`: https://github.com/mher/flower


Configuring the Stack
---------------------

The majority of services above are configured through the use of environment variables. Just check out :ref:`envs` and you will know the drill.

To obtain logs and information about crashes in a production setup, make sure that you have access to an external Sentry instance (e.g. by creating an account with `sentry.io`_), and set the ``SENTRY_DSN`` variable. Logs of level `logging.ERROR` are sent as Sentry events. Therefore, in order to send a Sentry event use:

.. code-block:: python

    import logging
    logging.error("This event is sent to Sentry", extra={"<example_key>": "<example_value>"})

The `extra` parameter allows you to send additional information about the context of this error.


You will probably also need to setup the Mail backend, for example by adding a `Mailgun`_ API key and a `Mailgun`_ sender domain, otherwise, the account creation view will crash and result in a 500 error when the backend attempts to send an email to the account owner.

.. _sentry.io: https://sentry.io/welcome
.. _Mailgun: https://mailgun.com


(Optional) Postgres Data Volume Modifications
---------------------------------------------

Postgres is saving its database files to the ``production_postgres_data`` volume by default. Change that if you want something else and make sure to make backups since this is not done automatically.


Building & Running Production Stack
-----------------------------------

You will need to build the stack first. To do that, run::

    docker-compose -f platform.prod.yml build

Once this is ready, you can run it with::

    SERVER_NAME=<server_name> docker-compose -f platform.prod.yml up

    # <server_name> is something like, platform.ld-investment.ai

To run the stack and detach the containers, run::

    SERVER_NAME=<server_name> docker-compose -f platform.prod.yml up -d

To run a migration, open up a second terminal and run::

   docker-compose -f platform.prod.yml run --rm django python manage.py migrate

To create a superuser, run::

   docker-compose -f platform.prod.yml run --rm django python manage.py createsuperuser

If you need a shell, run::

   docker-compose -f platform.prod.yml run --rm django python manage.py shell

To check the logs out, run::

   docker-compose -f platform.prod.yml logs

If you want to scale your application, run::

   SERVER_NAME=<server_name> docker-compose -f platform.prod.yml up --scale django=4
   SERVER_NAME=<server_name> docker-compose -f platform.prod.yml up --scale celeryworker=2

.. warning:: don't try to scale ``postgres``, ``celerybeat``, or ``traefik``.

To see how your containers are doing run::

    docker-compose -f platform.prod.yml ps


Example: Supervisor
-------------------

Once you are ready with your initial setup, you want to make sure that your application is run by a process manager to
survive reboots and auto restarts in case of an error. You can use the process manager you are most familiar with. All
it needs to do is to run ``docker-compose -f platform.prod.yml up`` in your projects root directory.

If you are using ``supervisor``, you can use this file as a starting point::

    [program:{{cookiecutter.project_slug}}]
    command=docker-compose -f platform.prod.yml up
    directory=/path/to/{{cookiecutter.project_slug}}
    redirect_stderr=true
    autostart=true
    autorestart=true
    priority=10

Move it to ``/etc/supervisor/conf.d/{{cookiecutter.project_slug}}.conf`` and run::

    supervisorctl reread
    supervisorctl update
    supervisorctl start {{cookiecutter.project_slug}}

For status check, run::

    supervisorctl status
