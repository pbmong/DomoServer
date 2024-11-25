FROM python:3.11

WORKDIR /backend/

COPY . .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r requirements.txt

# python libraries installation
# RUN python -m pip install mysql-connector-python
# RUN python -m pip install paho-mqtt
# RUN python -m pip install urllib3
# RUN python -m pip install fastapi
# RUN python -m pip install uvicorn

CMD python -m uvicorn API_backend:app --reload --host 0.0.0.0 --port 80 


# ATTENTION: after docker startup, backend launcher needs to be executed manually with the following command:
# python main.py
