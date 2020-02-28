FROM python:3.8.1-alpine

RUN adduser -D shield_api

WORKDIR /home/shield_api

RUN apk update
RUN apk add postgresql-dev gcc python3-dev musl-dev

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install --upgrade pip
RUN venv/bin/pip install -r requirements.txt

COPY app app
COPY shield_api.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP shield_api.py
RUN apk add --no-cache gcc musl-dev linux-headers

RUN chown -R shield_api:shield_api ./

# Add wait-for-it
COPY wait-for-it.sh wait-for-it.sh 
RUN apk add --no-cache bash
RUN chmod +x wait-for-it.sh
USER shield_api

EXPOSE 5000
# ENTRYPOINT ["./boot.sh"]

# ENTRYPOINT ["./wait-for-it.sh" , "localhost:5432", "--strict" , "--timeout=10" , "--" , "./boot.sh"]
ENTRYPOINT ["./wait-for-it.sh" , "localhost:5432", "--timeout=10" , "--" , "./boot.sh"]