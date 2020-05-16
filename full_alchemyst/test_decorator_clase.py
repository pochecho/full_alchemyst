import pprint
try :
    import __builtin__
except: 
    # Python 3.x
    import builtins

try : 
    builtin_types = [t for t in __builtin__.__dict__.itervalues() if isinstance(t, type)]
except:
    builtin_types = [getattr(builtins, d) for d in dir(builtins) if isinstance(getattr(builtins, d), type)]
def apply_defaults(cls):
    defaults = {
        'default_value1':True,
        'default_value2':True,
        'default_value3':True,
    }
    for name, value in defaults.items():
        setattr(cls, name, True)
    return cls

@apply_defaults
class Settings(object):
    pass

a = Settings()

attributes =  [
    {
        "name":"id",
        "type":"int",
        "primary_key":True
    },
    {
        "name":"protons",
        "type":"str"
    },
    {
        "name":"electrons",
        "type":"str"
    }
]

TYPE  = "type"
NAME = "name"
class Entity(object):

    

    def __init__(self, alchemyst_type,attributes):
        self.alchemyst_type = alchemyst_type
        self.attributes = attributes

    def get_default_value(self,attribute):
        print(789978,self.alchemyst_type)
        print(780008,self.alchemyst_type.__name__)
        try:
            key = self.alchemyst_type.__name__
            return self.get_config_attribute_mongo(attribute)
        except:
            return self.alchemyst_type
        """
        try:
            return next(filter(lambda x: x.__name__ == attribute[TYPE],builtin_types ))()
        except:
            pass
        """
    def get_config_attribute_mongo(self,attribute):
        pprint.pprint(attribute)
        print(attribute[TYPE])
        a = {
            "str": lambda : self.alchemyst_type.StringField(),
            "int" : lambda : self.alchemyst_type.IntField()
        }.get(attribute[TYPE],lambda: self.alchemyst_type.StringField())()
        print("Intrusión ", a)
        return a

    def __call__(self, cls):
        for attribute in self.attributes:
            val = self.get_default_value(attribute)
            print("Este es el valor",val)
            setattr(cls, attribute[NAME], val)
        return cls
"""
@Entity(alchemyst_type=None, attributes = attributes)
class Atom(object):
    def __init__(self):
        pass

if __name__ == "__main__":
    a = Atom()
    print(a.protons)
    print(a.electrons)
    print(a.id)
"""