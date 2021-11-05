FROM python:latest

WORKDIR /home/app
COPY . .
RUN pip install cherrypy

ENTRYPOINT ["python", "main.py"]

EXPOSE 8080