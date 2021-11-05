import cherrypy
from libs.base import Base
from os import path, mkdir
from socket import gethostbyname, gethostname


class Main(object):
    def __init__(self, host, port):
        self.base = Base()
        self.host = host
        self.port = int(port)

        if self.host is None:
            self.host = gethostbyname(gethostname())

        cherrypy.config.update({
            'server.socket_host': self.host,
            'server.socket_port': self.port,
            'engine.autoreload.on': False,
            'log.access_file': path.join("logs", "access.log"),
            'log.error_file': path.join("logs", "error.log"),
            'environment': 'production'
        })

        print(f"Running at: http://{self.host}:{self.port}")


    @cherrypy.expose
    def index(self):
        with open(path.join('templates', 'index.html'), 'r', encoding="utf-8") as f:
            return f.read()

    @cherrypy.expose
    def addData(self, temp, hum):
        if self.base.addData(temp, hum):
            return ""
        else:
            raise cherrypy.HTTPError(400)

    @cherrypy.expose
    def getData(self):
        return self.base.getData()


def start_server(host=None, port=8080):
    if not path.isdir('logs'):
        mkdir('logs')

    cherrypy.quickstart(Main(host, port))
