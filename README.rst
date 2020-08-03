Mood Music
==========

.. image:: https://img.shields.io/badge/License-GPLv3-blue.svg
    :target: https://www.gnu.org/licenses/gpl-3.0
    :alt: GNU GPLv3 License
.. image:: https://img.shields.io/badge/built%20with-Cookiecutter%20Django-ff69b4.svg
     :target: https://github.com/pydanny/cookiecutter-django/
     :alt: Built with Cookiecutter Django
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
     :target: https://github.com/ambv/black
     :alt: Black code style


This Django project is being built as a participant management and data collection platform the Mood Music study.
The project will integrate with the Twilio and Spotify APIs to send participant questionnaires via SMS, whilst also collecting
their authorised Spotify data.


Dev Guidelines
---------------

General logging and recording of tasks will be done through the GitHub project board. Ask @ninadicara if you have any questions.

Requirements
^^^^^^^^^^^^^
The requirements files can be found in ``/requirements``.
It is the responsibility of contibutors to maintain the requirements file with any new packages.


Style
^^^^^^
``black`` and ``flake8`` are the preferred Python formatting and style standards for this project, with the exception of line length
going up to 119 characters (the length of GitHub's code review). Further advice on code style for Django can be found here_.
Installing the pre-commit hook that has been set up on the repo will ensure that Python code meets this standard before being pushed.

To install the pre-commit git hook:
.. code-block::
  pip install pre-commit
  pre-commit install

.. _here: https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/

Documentation
^^^^^^^^^^^^^^
Documentation of code is the responsibility of all contributors. Please follow `NumPy conventions`_ for inline documentation, particuarly
docstrings.
Spynx will be used for autogeneration of documentation, so ``.rst`` (reStructuredText_) files are preferred over ``.md``.

.. _NumPy conventions: https://numpydoc.readthedocs.io/en/latest/format.html
.. _reStructuredText: https://restructuredtext-philosophy.readthedocs.io/en/latest/index.html

Branches
^^^^^^^^^
This project will follow the principles of the GitFlow_, meaning that the main branch is only used for stable releases. To develop any new features
please use a feature branch from ``develop`` with the naming convention ``feature/name-of-feature``.

Please note that ``main`` is a protected branch, and cannot be pushed to without a reviewed pull request from ``develop``.

.. _GitFlow: https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow

External Contributors
^^^^^^^^^^^^^^^^^^^^^^
External contributors are very welcome! Please fork the repo and submit a pull request to ``develop``.
PRs will be reviewed by @ninadicara and/or @leriomaggio.
