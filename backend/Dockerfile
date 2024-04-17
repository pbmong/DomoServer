FROM python:3.11

WORKDIR /backend/

COPY . .

RUN pip install --upgrade pip

# python libraries installation
RUN python -m pip install mysql-connector-python
RUN python -m pip install paho-mqtt
RUN python -m pip install urllib3


CMD python ./mqtt_listener_to_ddbb.py


#building command: docker build -t domoserver-backend:latest ./backend
#container creation:  docker run --network DomoServer_network --name DomoServer-backend domoserver-backend:latest 
#network setup: docker network create DomoServer_network
