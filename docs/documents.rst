Documents
=========

This project uses Sphinx_ documentation generator.

After you have set up to `develop locally`_, run the following command from the project directory to build and serve HTML documentation: ::

    $ make -C docs livehtml

If you set up your project to `develop locally with docker`_, run the following command: ::

    $ docker-compose -f local.yml up docs

Navigate to port 7000 on your host to see the documentation. This will be opened automatically at `localhost`_ for local, non-docker development.

Note: using Docker for documentation sets up a temporary SQLite file by setting the environment variable ``DATABASE_URL=sqlite:///readthedocs.db`` in ``docs/conf.py`` to avoid a dependency on PostgreSQL.

Generate API documentation
----------------------------

Edit the ``docs`` files and project application docstrings to create your documentation.

Sphinx can automatically include class and function signatures and docstrings in generated documentation.
See the generated project documentation for more examples.

Drawing Diagram
----------------------------

We use `sphinx-contrib/kroki`_ to produce various diagram in Sphinx framework.
Just create whatever diagram you want in any ``.rst`` file like below. ::

    .. kroki::
        :caption: I am an example!
        :type: plantuml

        @startuml
        Alice -> Bob: Authentication Request
        Bob --> Alice: Authentication Response

        Alice -> Bob: Another authentication Request
        Alice <-- Bob: Another authentication Response
        @enduml


This will produce diagram like below.

.. kroki::
    :caption: I am an example!
    :type: plantuml

    @startuml
    Alice -> Bob: Authentication Request
    Bob --> Alice: Authentication Response

    Alice -> Bob: Another authentication Request
    Alice <-- Bob: Another authentication Response
    @enduml

Make sure you change ``type`` of diagram and write code accordingly. You may refer `Kroki use-cases`_ example for this.

Setting up ReadTheDocs
----------------------

To setup your documentation on `ReadTheDocs`_, you must

1. Go to `ReadTheDocs`_ and login/create an account
2. Add your GitHub repository
3. Trigger a build

Additionally, you can auto-build Pull Request previews, but `you must enable it`_.

.. _localhost: http://localhost:7000/
.. _Sphinx: https://www.sphinx-doc.org/en/master/index.html
.. _develop locally: ./developing-locally.html
.. _develop locally with docker: ./developing-locally-docker.html
.. _sphinx-contrib/kroki: https://github.com/sphinx-contrib/kroki
.. _Kroki use-cases: https://kroki.io/examples.html#use-case
.. _ReadTheDocs: https://readthedocs.org/
.. _you must enable it: https://docs.readthedocs.io/en/latest/guides/autobuild-docs-for-pull-requests.html#autobuild-documentation-for-pull-requests
