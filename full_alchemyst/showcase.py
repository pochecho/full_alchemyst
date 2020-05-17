from full_alchemyst import define, FullAlchemyst
from flask import Flask
db_config = {
    "type":"mysql",
    "driver": "pymysql",
    "host": "localhost",
    "port":3306,
    "user":"root",
    "database":"google",
    "password":"Sifamek!666"
}
"""
db_config = {
    "type":"mongo",
    "host": "localhost",
    "port":27017,
    "user":"",
    "database":"google",
    "password":"",
    "SQLALCHEMY_TRACK_MODIFICATIONS":True
}
"""
app = Flask(__name__)
fullAlchemyst= FullAlchemyst(app,db_config)

class task(fullAlchemyst.Entity):
    id = define(fullAlchemyst.db, {"name":"id","type":"int","primary_key":True})
    nombre = define(fullAlchemyst.db, {"name":"nombre","type":"str"})

vue = {"nombre":"Ejercitar muela","id":41}
at = task(**vue)
fullAlchemyst.add(at)
