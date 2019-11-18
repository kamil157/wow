https://wow-simc.herokuapp.com/

This project is a Django website which generates input for SimulationCraft based on the cartesian product of
selected talents.
It generates both copy=... and profileset... settings.

.. image::example.png

Installation notes:

- Install `Python <https://www.python.org/>`_
- Install and activate `virtualenv <https://virtualenv.pypa.io/en/stable/>`_
- Install `requirements.txt <https://pip.pypa.io/en/stable/user_guide/#requirements-files>`_
- Set environment variables environment_
- Run server: python manage.py runsslserver
- Use a web browser to connect to development server (https://127.0.0.1:8000 by default)

.. _environment:

Environment variables:

+----------------------+---------------------------------------------------------------------------------------------+
| Name                 | Description                                                                                 |
+======================+=============================================================================================+
| DJANGO_CONFIGURATION | 'Dev' or 'Prod'                                                                             |
+----------------------+---------------------------------------------------------------------------------------------+
| DJANGO_SECRET_KEY    | `Django doc <https://docs.djangoproject.com/en/1.11/ref/settings/#std:setting-SECRET_KEY>`_ |
+----------------------+---------------------------------------------------------------------------------------------+
| WOW_API_CLIENT_ID    | Client id for battle.net API                                                                |
+----------------------+---------------------------------------------------------------------------------------------+
| WOW_API_CLIENT_SECRET| Secret key used for battle.net API                                                          |
+----------------------+---------------------------------------------------------------------------------------------+
| EMAIL_ADDRESS        | Email address from which email messages are sent                                            |
+----------------------+---------------------------------------------------------------------------------------------+
| EMAIL_PASSWORD       | Password to the above email address                                                         |
+----------------------+---------------------------------------------------------------------------------------------+
