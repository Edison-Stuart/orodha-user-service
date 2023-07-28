# orodha-user-service

This service will handle the creation/storage of users and the interaction with the keycloak api for the Orodha app.

## Usage & Requirements

In order to use this repository there are some conditions that have to be met. You must have a `.env` file containing:

- DOCKER_USERNAME
- DOCKER_PASSWORD
- TAG
- DBROOTUSER
- DBROOTPASSWORD
- DBUSER
- DBPASSWORD
- DBNAME
  The `docker-compose.main.yaml` file uses these variables in order to build the image using the Dockerfile as well as set up the database.

The Dockerfile has an argument called `REQUIREMENTS_FILE` that is by default set to `requirements.txt`. For now, this can only be changed by setting an environment variable named REQUIREMENTS_FILE to the requirement file that you would like to use.

This repository contains a secondary requirements file named `dev_requirements.txt`. This file contains the tools that are required to not only run, but also test the application. In the future there are plans to utilize the profiles function of docker-compose to launch with a different requirement file depending on if the app is being run in development or production.
