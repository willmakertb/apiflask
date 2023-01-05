import uuid
import threading

import requests

from flask_mysqldb import MySQL
from flaskext.mysql import MySQL
from .config import Config

import sqlalchemy

import json
import os
from flask import jsonify

pwd = Config.PASSWORD

db = None

db_user =  'william'
db_pass =  'Tappan930'
db_name =  'servidoriot'
db_host =  '127.0.0.1'
db_port =  '3306'

def config(app):
    app.config['MYSQL_HOST'] = 'localhost'
    app.config["MYSQL_USER"] = "william"
    app.config["MYSQL_PASSWORD"] =pwd
    app.config["MYSQL_DB"] = "servidoriot"
    app.config["MYSQL_PORT"] = 3306

    global mysql
    mysql = MySQL(app)
    return mysql





def call_procedure_sql():
    # Obtiene un cursor para la base de datos
    cursor = mysql.get_db().cursor()

    # Ejecuta la stored procedure
    cursor.callproc('get_data')

    # Realiza alguna acción con los resultados de la stored procedure
    result = cursor.fetchall()
    for row in result:
        print(row)

    # Cierra el cursor y la conexión a la base de datos
    cursor.close()
    mysql.get_db().close()



def connect():
    global db
    db = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            database=db_name,
            host=db_host,
            port=db_port
        ),
        pool_size=10,
        max_overflow=5,
        pool_timeout=30,
        pool_recycle=1800
    )


class DataBase():
    def __init__(self):
        pass


    def __preprocData(self,data,returnOne=False,multi_line=False):
        if (multi_line == True):
            data=[json.loads(x[0]) for x in data]
            if (returnOne == True and len(data)): return data[0]
        else:
            if (len(data[0]) > 0):
                data=data[0]
                data=json.loads(data[0])
                if (returnOne): return data[0]
            else:
                data = json.loads(data)
                if (returnOne and len(data) > 0): return data[0]
        return data


    def call_procedure_records(self, name, args=[], value=None, type='0'):
        try:
            connect()

            connection = db.raw_connection()

            cursor = connection.cursor()
            print(value)
            cursor.callproc(name, [value])
            print('cursos', cursor)
            records = cursor.fetchall()
            records = self.__preprocData(records)
            print('records', records)

            cursor.close()
            connection.commit()
            try:
                connection.close()
            except:
                pass
            return records
        except Exception as e:
            print("ERROR 1 => {}".format(e))
            try:
                connection.close()
            except:
                pass
            return {"ERROR 2": "{}".format(e)}
        finally:
            connection.close()


    def querymysql(self):
        connect()
        connection = db.raw_connection()
        cursor = connection.cursor()
        return cursor
