# full_alchemyst
Let's you to use both SqlAlchemyst and MongoAlchemyst libraries
Les's to use a unique ORM to manage the persistence in one project. 

## How to Use?
You need to configurate a dictionary with the next parameters:
db_config = {
    "type":"mongo",
    "host": "localhost",
    "port":27017,
    "user":"",
    "database":"google",
    "password":"",
    "SQLALCHEMY_TRACK_MODIFICATIONS":True
}

- *** type: ***  mongo | mysql
- *** host: ***  Host where the database is
- *** port: ***  Port of engine runs
- *** user: ***  User
- *** databse: ***  Name of database
- *** password: ***  Password

How you see, you can to specify other attributes of the ORM, like "SQLALCHEMY_TRACK_MODIFICATIONS".

After to set the configuration that you want to use, you have to create a FullAlchemyst instance:

```
app = Flask(__name__)
fullAlchemyst= FullAlchemyst(app,db_config)
```

Obviusly, What is a ORM without models? Create one:

```
class task(fullAlchemyst.Entity):
    id = define(fullAlchemyst.db, {"name":"id","type":"int","primary_key":True})
    nombre = define(fullAlchemyst.db, {"name":"nombre","type":"str"})
```

### Steps:
1. First, you need to extend you model of fullAlchemyst.Entity
2. Define your attributes. In this step, remember to use the "define" function. We see this later

### "define" function
This function is used to configurate you model depending what type of database you use.

This function, receives a dict, and its structure is the next:
- type : int | str o another inside de buildins of python.
- primary_key : If you attribute is a primary key.