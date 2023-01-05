from tools.databases import config, DataBase

import unittest

import os
from flask import jsonify
from app import create_app
from flask_swagger_ui import get_swaggerui_blueprint



app = create_app()



mysql = config(app)

dir_file = os.path.join(os.path.dirname(__file__), 'app/static', "openapi.json")

SWAGGER_URL = '/api'
API_URL = 'http://127.0.0.1:5050/static/openapi.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "apiflask",
        "docExpansion": "none",
        "filter": ''
    }
)

db = DataBase()

app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

''' 
@app.route("/api", methods=['GET'])
def swagger_ui():
    try:
        return render_template('swagger_ui.html')
    except Exception as e:
        return jsonify({"Error": "swagger_ui", "Exception":"Error {}".format(e)})

'''


@app.route('/')
def  apitest():
    return "API FLASK en github "


@app.route('/get' ,  methods=['GET'])
def get():
    return "obeten data metodo get"

# routes
@app.route('/query')
def Index():
    cur = db.querymysql()
    cur.execute('SELECT id, name, username client_id FROM user')
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
        # Cierra el cursor y la conexión a la base de datos
        cursor.close()
        mysql.get_db().close()



    except Exception as e:
        return "Error en ", e


@app.route('/api-get' , methods=['GET', 'POST'])
def apiget():
    try:
        bodyJson = 1
        result = db.call_procedure_records('get_data', value=bodyJson )
        print('result', result)

        return jsonify(result)
    except Exception as e:
        dta = {
            "Error": "True",
            "message": "{}".format(e),
            "Data": None
        }
        return jsonify(dta)


@app.route('/user' , methods=['GET', 'POST'])
def user():
    try:
        bodyJson = 1
        result = db.call_procedure_records('get_data', value=bodyJson)
        print('result', result)

        return jsonify(result)
    except Exception as e:
        dta = {
            "Error": "True",
            "message": "{}".format(e),
            "Data": None
        }
        return jsonify(dta)

@app.cli.command()
def test():
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return "Error 404"


@app.errorhandler(500)
def server_error(error):
    return " Error 500"

if __name__ == "__main__":
    app.run(port=5050, debug=True)
