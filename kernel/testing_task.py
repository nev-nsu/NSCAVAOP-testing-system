from kernel.generate import *
from kernel.sandbox import Sandbox
from uuid import uuid4
import threading

class TestingTask:
    def __init__(self, code, options, tests, verifier, responce):
        self.status = 'added'
        self.code = code
        self.verifier = verifier
        self.options = options
        self.tests = tests
        self.responce = responce
        # generate a token
        self.number = uuid4()
        # create thread for the task
        self.worker = threading.Thread(target=self.execute)
        
    def start(self):
        self.worker.start()

    def execute(self):
        sb = Sandbox(self.number)
        # todo: transform options to string
        res = sb.compile_untrusted(self.code, self.options)
        if res.hasattr('error'):
            self.status = 'failed'
            self.result = res.error
            return
        self.status = 'compiled'
        gen = Generator(self.tests)
        self.status = 'run'
        try:
            for result in self.testing(sb, gen):
                if self.responce == 'statistics':
                    self.result[result.status] += 1
                elif self.responce == 'raw_data' or result.status != 'OK':
                    self.result.append(result)
            self.status = 'finished'
        except UnresolvedVariableName:
            self.status = 'failed'
            self.result = 'Bad test template: unresolved variable name'
        except UnknownType:
            self.status = 'failed'
            self.result = 'Bad test template: unknown type'
        except BadTemplate:
            self.status = 'failed'
            self.result = 'Bad test template'


    def testing(self, sandbox, generator):
        for test in generator.generate():
            result = {}
            result.input = test
            res = sandbox.execute_untrusted(test)
            if not res.hasattr('error'):
                result.output = sandbox.get_execution_result()
                res = sandbox.verify_untrusted(self.verifier, test)
                if not res.hasattr('error'):
                    result.status = res
                    yield result
            self.status = 'CRASH'
            self.result = res.error
            yield result
