FROM edisonstuart/orodha-base-image-prod:latest

ARG SERVER_USER=gunicorn-user
ARG PORT=5000

RUN adduser ${SERVER_USER} -G www-data -D
USER ${SERVER_USER}

COPY ./application /orodha-user-service/application
COPY ./scripts/server_scripts/server_start.sh /orodha-user-service

WORKDIR /orodha-user-service

CMD /orodha-user-service/server_start.sh  -u ${SERVER_USER} -p ${PORT}
