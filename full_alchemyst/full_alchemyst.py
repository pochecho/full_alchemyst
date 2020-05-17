DRIVER_CONFIG= {
    "mongo":{
        "module":"flask_mongoalchemy",
        "path":"MONGOALCHEMY_CONNECTION_STRING",
        "driver":"",
        "type":"mongodb",
        "attributes":{
            "MONGOALCHEMY_DATABASE":"<<database>>"
        }
    },
    "mysql": {
        "module":"flask_sqlalchemy",
        "path":"SQLALCHEMY_DATABASE_URI",
        "driver":"pymysql",
        "type":"mysql",
        "SQLALCHEMY_TRACK_MODIFICATIONS": "<<SQLALCHEMY_TRACK_MODIFICATIONS>>",
        "attributes":{
            "MONGOALCHEMY_DATABASE":False
        }
    }
}

TYPE  = "type"
NAME = "name"
MODULE = "module"
PATH = "path"
ATTRIBUTES = "attributes"

import importlib
from flask_mongoalchemy import MongoAlchemy
from flask_sqlalchemy import SQLAlchemy

def define(db,attribute):
    def get_default_value():
        try:
            key = db.__name__
            return get_config_attribute_mongo()
        except:
            return get_config_attribute_sql()
    def get_config_attribute_sql():
        return {
            "str": lambda : db.Column(db.String(100)),
            "int" : lambda : db.Column(db.Integer(), primary_key=True)
        }.get(attribute[TYPE],lambda: db.Column(db.String()))()
    def get_config_attribute_mongo():
        return {
            "str": lambda : db.StringField(),
            "int" : lambda : db.IntField()
        }.get(attribute[TYPE],lambda: db.StringField())()
    return get_default_value()


class FullAlchemyst(object):
    def __init__(self,app,db_config):
        self.app = app
        self.db_config=db_config
        self.Entity = None
        self.db = None
        self.alchemyst  = None
        self.connection_string = ""
        self.__config__()
    
    def __config__(self):
        SPECIFIC_ALCHEMYST = DRIVER_CONFIG[self.db_config[TYPE]]
        self.alchemyst = importlib.import_module(SPECIFIC_ALCHEMYST[MODULE])
        self.connection_string = self.__build_connection_string()
        attributes = self.__build_extra_attributes(SPECIFIC_ALCHEMYST)
        self.app.config[SPECIFIC_ALCHEMYST[PATH]] = self.connection_string
        for attribute in attributes:
            self.app.config[attribute] = attributes[attribute]
        self.db = self.__get_db()(self.app)
        self.Entity = self.__get_hierarchy()
    
    def __build_extra_attributes(self,specific_config):
        attrs = specific_config[ATTRIBUTES]
        for key in attrs:
            value = attrs[key]
            if type(value).__name__ == "str" and  ">>" in value:
                attrs[key] = self.db_config[value.replace(">>","").replace("<<","")]
            else:
                attrs[key] = value
        return attrs
    
    def __build_connection_string(self):
        specific_config = DRIVER_CONFIG[self.db_config["type"]]
        prefix = specific_config["type"]
        prefix = prefix if specific_config["driver"] == "" else prefix+"+"+specific_config["driver"]
        credentials = "{0}:{1}".format(self.db_config["user"],self.db_config["password"])
        credentials = "" if credentials == ":" else credentials
        connecion_string_pattern = '{0}://{1}@{2}/{3}' if credentials != "" else '{0}://{1}{2}/{3}' 
        connection_string = connecion_string_pattern.format(prefix,credentials,self.db_config["host"],self.db_config["database"])
        return connection_string
    
    def __get_db(self):
        return {
            "flask_mongoalchemy":lambda : self.alchemyst.MongoAlchemy,
            "flask_sqlalchemy": lambda : self.alchemyst.SQLAlchemy
        }.get(self.alchemyst.__name__,None)()
    
    def __get_hierarchy(self):
        try:
            key = self.db.__name__
            return self.db.Document
        except:
            return self.db.Model
    
    def add(self,model):
        try:
            self.db.create_all()
        except:
            pass
        self.db.session.add(model)
        try:
            self.db.session.commit()
        except:
            pass
