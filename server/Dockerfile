FROM python:latest

WORKDIR /home/app
ENV WIFI-TEMP=AUTH_HEADER
COPY . .
RUN pip install cherrypy
RUN pip install requests
ENTRYPOINT ["python", "main.py"]

EXPOSE 8080
