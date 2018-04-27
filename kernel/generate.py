class VariableRedefinition(Exception):
    pass

import random

class UnresolvedVariableName(Exception):
    pass

class BadTemplate(Exception):
    pass

class UnknownType(Exception):
    pass

class Generator:
    def __init__(self, tests):
        self.tests = tests

    def generate(self):
        try:
            for group in self.tests:
                if group.type == 'generated':
                    for i in range(group.number):
                        yield self.__generate_instance__(group.template)
                else:
                    raise UnknownType()
        except AttributeError:
            raise BadTemplate()
                

    def __generate_instance__(self, template):
        self.names = {}
        return self.__generate_recursive__(template)['representation']

    def __get_attribute__(self, obj, name, optional = False):
        if hasattr(obj, name):
            attr = getattr(obj, name)
        else:
            if not optional:
                raise BadTemplate()
            return None
        if attr.type == 'value':
            return attr.value
        elif attr.type == 'variable':
            if not hasattr(self.names, attr.name):
                raise UnresolvedVariableName()
            return self.names[attr.name]
        elif attr.type == 'test':
            return __generate_recursive__(attr.template)['raw']
        else:
            raise UnknownType()

    def __generate_recursive__(self, template):
        name = self.__get_attribute__(template, 'name', True)
        if self.__get_attribute__(template, 'type') == 'integer':
            max = self.__get_attribute__(template, 'max')
            min = self.__get_attribute__(template, 'min')
            num = random.randint(min, max)
            result = { 'raw': num, 'representation': str(num) }
        else:
            raise UnknownType()
        if name:
            if name in self.names:
                raise VariableRedefinition()
            self.names[name] = result['raw']
        return result
            
