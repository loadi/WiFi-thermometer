import os
import sqlite3
import json
import time

import requests


class Base:
    TABLE_STRUCTURE = """
        CREATE TABLE "measurements" (
            "id"	INTEGER,
            "temp"	REAL NOT NULL,
            "hum"	REAL NOT NULL,
            "date"	DATETIME DEFAULT current_timestamp,
            PRIMARY KEY("id" AUTOINCREMENT))"""

    BASE_PATH = os.path.join(os.path.abspath(os.getcwd()), "stuff", 'base.db')

    def __init__(self):
        self.__create_base()

    def addData(self, temp, hum):
        sql = "INSERT INTO measurements (temp, hum) VALUES (?, ?)"
        try:
            temp = float(temp)
            hum = float(hum)

            if temp == temp and hum == hum:  # temp and hum is not nan, lol wtf?
                self.__execute(sql, (temp, hum))
                self.__send_to_graphite(temp, hum)
                return True
        except:
            pass

        return False

    def getData(self):
        resp = {"labels": [], "temp": [], "hum": []}
        sql = "select temp, hum, strftime('%H:%M', date, '+3 hour')," \
              "strftime('%d.%m.%Y в %H:%M', date, '+3 hour') " \
              "from measurements where " \
              "cast(strftime('%d', date, '+3 hour') as integer) = cast(strftime('%d', 'now', '+3 hour') as integer)"

        for line in self.__execute(sql, fetch=True):
            resp["temp"].append(line[0])
            resp["hum"].append(line[1])
            resp["labels"].append(line[2])
            resp["lastUpdate"] = line[3]

        return json.dumps(resp, indent=2)

    def getDataByDate(self, date):
        resp = {"labels": [], "temp": [], "hum": []}
        sql = "select temp, hum, strftime('%H:%M', date)," \
              "strftime('%d.%m.%Y', date) " \
              "from measurements where " \
              f"'{date}' = strftime('%Y-%m-%d', date)"
        for line in self.__execute(sql, fetch=True):
            resp["temp"].append(line[0])
            resp["hum"].append(line[1])
            resp["labels"].append(line[2])
            resp["lastUpdate"] = line[3]

        return json.dumps(resp, indent=2)

    def __execute(self, sql, data=(), fetch=False):
        with sqlite3.connect(self.BASE_PATH) as conn:
            if fetch:
                cursor = conn.execute(sql)
                resp = cursor.fetchall()
                return resp

            else:
                cur = conn.cursor()
                cur.execute(sql, data)
                conn.commit()
                return True

    def __create_base(self):
        if not os.path.isfile(self.BASE_PATH):
            if not os.path.isdir('stuff'):
                os.mkdir('stuff')

            open(self.BASE_PATH, 'w').close()
            self.__execute(self.TABLE_STRUCTURE)

    def __send_to_graphite(self, temp, hum):
        url = "https://graphite-prod-24-prod-eu-west-2.grafana.net/graphite/metrics"

        payload = json.dumps([
            {
                "name": "measurements.temperature",
                "interval": 60,
                "value": temp,
                "time": int(time.time())
            },
            {
                "name": "measurements.hum",
                "interval": 60,
                "value": hum,
                "time": int(time.time())
            }
        ])

        if 'WIFI-TEMP' not in os.environ:
            return

        auth = os.environ['WIFI-TEMP']

        headers = {
            'Content-Type': 'application/json',
            'Authorization': f"Basic {auth}",
        }

        requests.request("POST", url, headers=headers, data=payload)
