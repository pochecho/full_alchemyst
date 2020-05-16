class Attribute:
    pass
TYPE  = "type"
NAME = "name"
class Entity(object):
    def __init__(self, alchemyst_type,attributes):
        self.alchemyst_type = alchemyst_type
        self.attributes = attributes

    def get_default_value(self,attribute):
        try:
            return next(filter(lambda x: x.__name__ == attribute[TYPE],builtin_types ))()
        except:
            pass

    def __call__(self, cls):
        for attribute in self.attributes:
            val = self.get_default_value(attribute)
            setattr(cls, attribute["name"], val)
        return cls

