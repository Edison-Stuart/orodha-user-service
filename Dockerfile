FROM python:3.11.4-slim-bookworm

ARG SERVER_USER=gunicorn-user
ARG REQUIREMENTS_FILE=requirements.txt
ARG PORT=5000
COPY ./${REQUIREMENTS_FILE} .

RUN apt-get update -y && \
	DEBIAN_FRONTEND=noninteractive TZ=Etc/UTC && \
	apt-get install -y python3-pip python3-dev && \
	useradd ${SERVER_USER} && \
	usermod -aG www-data ${SERVER_USER} && \
	pip install -r ${REQUIREMENTS_FILE} && \
	rm ${REQUIREMENTS_FILE}

COPY ./application /orodha-user-service/application
COPY ./scripts/server_scripts/server_start.sh /orodha-user-service
RUN chmod +x /orodha-user-service/server_start.sh 

WORKDIR /orodha-user-service

CMD /orodha-user-service/server_start.sh  -u ${SERVER_USER} -p ${PORT}
