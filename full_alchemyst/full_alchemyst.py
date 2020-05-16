import importlib
import json
import sys

from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask_marshmallow import Marshmallow
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy
from test_decorator_clase import Entity


app = Flask(__name__)
DRIVER_CONFIG_URL = "./driver.config.json";
with open(DRIVER_CONFIG_URL) as f:
    DRIVER_CONFIG = json.loads(f.read())

DB_CONFIG_URL = "../db.config-mongo.json";
with open(DB_CONFIG_URL) as f:
    DB_CONFIG = json.loads(f.read())


def build_extra_attributes(db_config,driver_config):
    specific_config = driver_config[db_config["type"]]
    attrs = specific_config["attributes"]
    for key in attrs:
        value = attrs[key]
        if type(value).__name__ == "str" and  ">>" in value:
            attrs[key] = db_config[value.replace(">>","").replace("<<","")]
        else:
            attrs[key] = value
    return attrs

def build_connection_string(db_config,driver_config):
    specific_config = driver_config[db_config["type"]]
    prefix = specific_config["type"]
    prefix = prefix if specific_config["driver"] == "" else prefix+"+"+specific_config["driver"]


    credentials = "{0}:{1}".format(db_config["user"],db_config["password"])
    credentials = "" if credentials == ":" else credentials

    connecion_string_pattern = '{0}://{1}@{2}/{3}' if credentials != "" else '{0}://{1}{2}/{3}' 
    connection_string = connecion_string_pattern.format(prefix,credentials,db_config["host"],db_config["database"])
    return connection_string

def get_db(alchemyst):
    return {
        "flask_mongoalchemy":lambda : alchemyst.MongoAlchemy,
        "flask_sqlalchemy": lambda : alchemyst.SQLAlchemy
    }.get(alchemyst.__name__,None)()
    
def get_hierarchy(db):
    try:
        key = db.__name__
        return db.Document
    except:
        return db.Model

SPECIFIC_ALCHEMYST = DRIVER_CONFIG[DB_CONFIG["type"]]
Alchemyst = importlib.import_module(SPECIFIC_ALCHEMYST["module"])

connecion_string = build_connection_string(DB_CONFIG,DRIVER_CONFIG)
attributes = build_extra_attributes(DB_CONFIG,DRIVER_CONFIG)

app.config[SPECIFIC_ALCHEMYST["path"]] = connecion_string
for attribute in attributes:
    app.config[attribute] = attributes[attribute]
#db = Alchemyst.MongoAlchemy(app)

db = get_db(Alchemyst)(app)

entity = get_hierarchy(db)

ma = Marshmallow(app)
print("-----",db)

attributes = [
    {
        "name":"id",
        "type":"int",
        "primary_key":True
    },
    {
        "name":"nombre",
        "type":"str"
    }
]
@Entity(alchemyst_type=db, attributes = attributes)
class task(entity):
    pass

"""
class task(entity):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(70))
    def __init__(self, nombre):
        self.nombre = nombre
"""
##db.create_all()

at = task()
at.nombre = "TOmen note"
at.id = 45
print(at.__dict__)

db.session.add(at)
#db.session.commit()
