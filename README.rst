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

To schedule a study create an instance of StudyMeta in the admin panel.
The parameters set by StudyMeta will trigger the scheduling of all EMA text message tasks, ongoing Spotify user data collection
and regular evening messages to participants to signpost them to wellbeing services. 
