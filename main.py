from flask import Flask
from flask_mysqldb import MySQL
from databases import config, call_procedure_sql, DataBase

import json
import os
from flask import jsonify
app = Flask(__name__)

mysql = config(app)

db = DataBase()

@app.route('/')
def  apitest():
    return "API FLASK en github "


@app.route('/get' ,  methods=['GET'])
def get():
    return "obeten data"

# routes
@app.route('/query')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT id, user, client_id FROM conexiones')
    data = cur.fetchall()
    cur.close()
    return str(data)


@app.route('/get_data', methods=['GET'])
def get_data():
    try:
        cursor = mysql.get_db().cursor()

        # Ejecuta la stored procedure
        cursor.callproc('get_data', None)

        # Realiza alguna acción con los resultados de la stored procedure
        #result = cursor.fetchall()
        result = cursor.fetchall()

        print(result)

        for row in result:
            print(row)
            indice = row
        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        mysql.get_db().close()

        return indice


    except Exception as e:
        return "Error en ", e


@app.route('/api-get' , methods=['GET', 'POST'])
def apiget():
    try:
        bodyJson = 1
        result = db.call_procedure_records('get_data', value=bodyJson  )
        print('result', result)

        return jsonify(result)
    except Exception as e:
        dta = {
            "Error": "True",
            "message": "{}".format(e),
            "Data": None
        }
        return jsonify(dta)



if __name__ == "__main__":
    app.run(port=5050, debug=True)
