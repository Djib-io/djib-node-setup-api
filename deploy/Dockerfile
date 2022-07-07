FROM python:3.10

WORKDIR /app

EXPOSE 80

COPY . /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["sh", "/app/deploy/start.sh"]
