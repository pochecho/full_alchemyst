#!/usr/bin/env python
#Se importa Flask, reqest y jsonify
from bson.json_util import dumps
from flask import Flask
from flask import jsonify
from flask import request
from flask import Response
from flask_mongoalchemy import MongoAlchemy
from flask_restful import abort
from flask_restful import Api
from flask_restful import reqparse
from flask_restful import Resource
from flask_marshmallow import Marshmallow

#Se importa MongoAlchemy
#Se importa dumps
#rom flask_restful import Resource, Api#Se instancia la clase de Flask, se configura el acceso
#a la base de datos mongodb a empleados
app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'empleados'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://localhost:27017/empleados'
#Se instancia mongoalchemy pasando la app.
db = MongoAlchemy(app)#Se asocia el API a la aplicacion
ma = Marshmallow(app)

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('nombre', 'sexo', 'edad',"dni")
task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
api = Api(app)
#Se crea la clase empleados la cual manejara los documentos.
class empleados(db.Document):
    nombre = db.StringField()
    sexo = db.StringField()
    edad = db.IntField()
    dni = db.IntField()
#Se define la funcion de pagina no encontrada.
@app.errorhandler(404)
def not_found(error=None):
    mensaje = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = Response(jsonify(mensaje),status=404,mimetype='application/json')    
    return resp#Clase EmpleadosList que permite listar los empleados o insertar un empledo.
#Se definen los metdos get y post
class EmpleadosList(Resource):
    #Se define el metodo get el cual devuelve un json con todos los empleados.
    def get(self):
        #Se realiza la busqueda y se devuelve el resultado, si existe un error de atributo (que el empleado no existe)
        #Se devuelve empleado no encontrado.
        consulta = empleados.query.all()
        resp =  tasks_schema.dump(consulta)
        return jsonify(resp)

    #base de datos mongoDB.
    def post(self):
        #args = parser.parse_args()
        #Se crea la instancia empleado de la clase empleados donde se
        #logra hacer la inserción de un empleado con el metodo save.    
        print(request.json)    
        nombre = str(request.json['nombre'])
        sexo = str(request.json['sexo'])
        edad = int(request.json['edad'])
        dni = int(request.json['dni'])
        empleado = empleados(nombre=nombre,sexo=sexo,edad=edad,dni=dni)
        empleado.save()        #Se retorna que el usuario fue agregado.
        ###
        consulta = empleados.query.all()
        listado = []
        for i in consulta:
            listado.append(i.wrap())
        resp =  Response(dumps(listado),status=201,mimetype='application/json')
        resp.headers['Link'] = 'http://blog.crespo.org.ve'
        return resp#Se crea la Clase Empleado que hereda de Resource
#Tiene los metodos get, put y delete
class Empleado(Resource):
    #Se define el metodo get, permite buscar un empleado por su nombre
    def get(self,nombre):
        #Se realiza la busqueda y se devuelve el resultado, si existe un error de atributo (que el empleado no existe)
        #Se devuelve empleado no encontrado.
        try:
            resultado = empleados.query.filter(empleados.nombre == nombre).first()
            return dumps({'nombre':resultado.nombre,'sexo':resultado.sexo,'edad':resultado.edad,'dni':resultado.dni}),200,{'Content-Type':'application/json'}
        except (AttributeError):
            return not_found
    #Se define el metodo put que permite actualizar la informacion de un empleado
    #pasando su nombre, los datos a modificar se pasan en un json.
    def put(self,nombre):
        #Se intenta buscar al empleado en la base de datos, si no esta devuelve error
        try:
            #Se consulta en la base de datos, donde devuelve el primer elemento encontrado
            resultado = empleados.query.filter(empleados.nombre == nombre).first()
            #Se toma los datos de un json y se guardan en sus variables, salvando luego
            #en la base de datos.
            resultado.sexo = str(request.json['sexo'])
            resultado.edad = int(request.json['edad'])
            resultado.dni = int(request.json['dni'])
            resultado.save()
            #Se realiza la consulta desplegando los empleados
            consulta = empleados.query.all()
            listado = []
            for i in consulta:
                listado.append(i.wrap())
            #Se devuelve la nueva lista de empleados en un json.
            resp =  Response(dumps(listado),status=201,mimetype='application/json')
            resp.headers['Link'] = 'http://blog.crespo.org.ve'
            return resp
        except (AttributeError):
            return not_found    #Se define el metodo delete que permite borrar un empleado de la base de datos
    #pasando el nombre del empleado.
    def delete(self,nombre):
        #Se busca el empleado, si existe se borra de la base de datos y se devuelve
        #mensaje de empleado borrado, si no, se devuelve el mensaje de empleado no
        #encontrado.
        try:
            resultado = empleados.query.filter(empleados.nombre == nombre).first()
            resultado.remove()
            ###
            consulta = empleados.query.all()
            listado = []
            for i in consulta:
                listado.append(i.wrap())
            resp =  Response(dumps(listado),status=200,mimetype='application/json')
            resp.headers['Link'] = 'http://blog.crespo.org.ve'
            return resp
        except (AttributeError):
            return not_found#Se define las rutas para los recursos con las clases asociadas:
#/empleado
#/empleado/<string:nombre>
api.add_resource(EmpleadosList,'/empleado')
api.add_resource(Empleado,'/empleado/<string:nombre>')
if __name__ == "__main__":
    #Se corre la aplicacion en modo debug
    app.run(host="0.0.0.0",debug=True, port=5001)
