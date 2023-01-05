

from tools.databases import config, DataBase

from flask import  jsonify

db = DataBase()

def get_users(name):
        try:
            cur = db.querymysql()
            getuser = """SELECT username, name , password from user where name='{}' """.format(name)
            cur.execute(getuser)

            rv = cur.fetchone()

            print(rv)
            return (rv)

        except Exception as e:
            dta = {
                "Error": "True",
                "message": "{}".format(e),
                "Data": None
            }
            return jsonify(dta)