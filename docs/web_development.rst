(WIP) Web Development
==========================================

.. index:: web, local

The steps below will get you up and running with a ld_platform Web local development environment.

Local Development
------------------

To install npm packages, please do::

    npm install

This will install all the frameworks defined in `package.json` and trigger `npm run prepare`.
Pre-commit git hook framework for web development, husky will be installed.

After installation, to run webpack server::

    npm run start

You will be directed to the live web server on the browser.

If you made a change in codes and want to lint using `prettier` and `eslint`,::

    npm run lint

Thanks to husky, `npm run lint` will automatically performed even if you forgot to run lint
before making a git commit.
