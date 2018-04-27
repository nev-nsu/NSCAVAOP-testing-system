from kernel.generate import *
from kernel.sandbox import Sandbox
from uuid import uuid4
import threading

class TestingTask:
    def __init__(self, code, options, tests, verifier, response):
        self.status = 'added'
        self.code = code
        self.verifier = verifier
        self.options = options
        self.tests = tests
        self.response = response
        # generate a token
        self.number = str(uuid4())
        # create thread for the task
        self.worker = threading.Thread(target=self.execute)
        
    def start(self):
        self.worker.start()

    def execute(self):
        sb = Sandbox(self.number)
        res = sb.compile_untrusted(self.code, self.options)
        if 'error' in res:
            self.status = 'failed'
            self.result = res['error']
            return
        self.status = 'compiled'
        gen = Generator(self.tests)
        self.status = 'run'
        try:
            if self.response == 'statistics':
                self.result = {}
            else:
                self.result = []
            for result in self.testing(sb, gen):
                if self.response == 'statistics':
                    self.result[result['status']] += 1
                elif self.response == 'raw_data' or result['status'] != 'OK':
                    self.result.append([result])
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
            result = { 'input': test }
            res = sandbox.execute_untrusted(test)
            if 'error' in res:
                self.status = 'CRASH'
                self.result = res['error']
                yield result
            else:
                result['output'] = sandbox.get_execution_result()
                res = sandbox.verify_untrusted(self.verifier, test)
                if 'error' in res:
                    self.status = 'CRASH'
                    self.result = res['error']
                    yield result
                else:
                    result['status'] = res
                    yield result
