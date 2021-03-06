import random
import string

def representation(x):
    if isinstance(x, float):
        return str(x)
    if isinstance(x, int):
        return str(x)
    if isinstance(x, str):
        return x
    if isinstance(x, list):
        return ''.join([representation(i) for i in x])
    assert False, "Bad type of object in result"


class VariableRedefinition(Exception):
    def __init__(self, name):
        message = "Variable redefinition: '" + name + "'"
        super().__init__(message)


class UnresolvedVariableName(Exception):
    def __init__(self, name):
        message = "Unknown variable: '" + name + "'"
        super().__init__(message)


class BadTemplate(Exception):
    def __init__(self, message):
        message = "Bad template: " + message
        super().__init__(message)

class TooShortArray(Exception):
    def __init__(self):
        message = "Bad template: too short array"
        super().__init__(message)

class UnknownType(Exception):
    def __init__(self, name):
        message = "Unknown type: '" + name + "'"
        super().__init__(message)

# Use it!


class BadParameterType(Exception):
    def __init__(self):
        message = "Bad template: wrong parameter type"
        super().__init__(message)


class MissingParameter(Exception):
    def __init__(self, name):
        message = "Bad template: not optional parameter '" + name + "' is missing"
        super().__init__(message)


class TGenerator:
    def __init__(self, tests):
        self.tests = tests

    def generate(self):
        try:
            for group in self.tests:
                for _ in range(group['number']):
                    yield self.__generate_instance__(group['template'])
        except (AttributeError, KeyError) as e:
            raise BadTemplate(str(e))
        except Exception as e:
            print(e)
            raise e

    def __generate_instance__(self, template):
        self.names = {}
        res = self.__generate_recursive__(template)
        return representation(res)

    def __get_attribute__(self, obj, name, optional=False):
        if name in obj:
            attr = obj[name]
        else:
            if not optional:
                raise MissingParameter(name)
            return None
        if attr['type'] == 'value':
            return attr['value']
        elif attr['type'] == 'variable':
            if not attr['name'] in self.names:
                raise UnresolvedVariableName(attr['name'])
            return self.names[attr['name']]
        elif attr['type'] == 'test':
            return self.__generate_recursive__(attr['template'])
        else:
            raise UnknownType(attr['type'])

    def __generate_recursive__(self, template):
        name = self.__get_attribute__(template, 'name', True)
        type = self.__get_attribute__(template, 'type')
        if type == 'integer':
            max = self.__get_attribute__(template, 'max')
            min = self.__get_attribute__(template, 'min')
            num = random.randint(min, max)
            result = num
        elif type == 'real':
            max = self.__get_attribute__(template, 'max')
            min = self.__get_attribute__(template, 'min')
            num = random.uniform(min, max)
            result = num
        elif type == 'string':
            length = self.__get_attribute__(template, 'length')
            allowed = self.__get_attribute__(template, 'allowed', True)
            forbidden = self.__get_attribute__(template, 'forbidden', True)
            if allowed:
                result = ''.join(random.choice(allowed) for _ in range(length))
            elif forbidden:
                result = ''.join(
                    random.choice(
                        (string.ascii_uppercase +
                         string.digits).translate(
                             None,
                             forbidden)) for _ in range(length))
            else:
                raise MissingParameter('allowed/forbidden')
        elif type == 'array':
            length = self.__get_attribute__(template, 'length')
            inner = self.__get_attribute__(template, 'element_type')
            result = [self.__generate_recursive__(inner) for _ in range(length)]
        elif type == 'composite':
            array = self.__get_attribute__(template, 'array')
            if len(array) < 1:
                raise TooShortArray()
            result = [self.__generate_recursive__(x) for x in array]
        elif type == 'choice':
            array = self.__get_attribute__(template, 'array')
            if len(array) < 1:
                raise TooShortArray()
            inner = random.choice(array)
            result = self.__generate_recursive__(inner)
        elif type == 'const':
            result = self.__get_attribute__(template, 'value')
        else:
            raise UnknownType(type)
        if name:
            if name in self.names:
                raise VariableRedefinition(name)
            self.names[name] = result
        return result
