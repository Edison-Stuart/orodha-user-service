# orodha-user-service

This service will handle the creation/storage of users and the interaction with the keycloak api for the Orodha app.

## Usage & Requirements

In order to use this repository there are some conditions that have to be met. You must have a `.env` file containing:

-   DOCKER_USERNAME
-   DOCKER_PASSWORD
-   TAG
-   DBROOTUSER
-   DBROOTPASSWORD
-   DBUSER
-   DBPASSWORD
-   DBNAME
-   DBHOSTNAME
-   DBPORTS
-   KEYCLOAK_SERVER_URL
-   KEYCLOAK_REALM_NAME
-   KEYCLOAK_CLIENT_ID
-   KEYCLOAK_CLIENT_SECRET_KEY

    The `docker-compose.main.yaml` file uses these variables in order to build the image using the Dockerfile as well as set up the database.

### API

There are four `/users` routes as well as one `/main` route.

The `/users` routes are the main purpose of this service, this url supports GET, DELETE, and POST requests at the current
moment.

For GET and DELETE requests you can pass a user_id into the route like so:

```
/users/<string:user_id>/
```

GET will return a specific user if you have access
DELETE will remove a user from keycloak and mongoDB.

Without a user_id, the DELETE route will not accept the request.

A GET request without a user_id value will return a list of all users containing
only the id, keycloak_id, and username of each user.

The POST request does not expect an id in the route, just a form body like a typical POST request.

These routes also expect the headers of

```
{"Content-Type": "application/json"}
```

and

```
{"Authorization": "Bearer {some user token provided by keycloak}"}
```

The Dockerfile has an argument called `REQUIREMENTS_FILE` that is by default set to `requirements.txt`. For now, this can only be changed by setting an environment variable named REQUIREMENTS_FILE to the requirement file that you would like to use.

This repository contains a secondary requirements file named `dev_requirements.txt`. This file contains the tools that are required to not only run, but also test the application. In the future there are plans to utilize the profiles function of docker-compose to launch with a different requirement file depending on if the app is being run in development or production.
