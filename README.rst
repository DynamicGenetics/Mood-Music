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


Useful commands to remember
---------------------------

Creating fixtures after populating database
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`python manage.py dumpdata --format=json survey.survey survey.category survey.question > "moodmusic/fixtures/survey/survey_init.json"`  
`python manage.py dumpdata --format=json ema.emaquestions > "moodmusic/fixtures/ema/ema_init.json"`                                              ─╯

