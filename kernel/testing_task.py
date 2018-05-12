from uuid import uuid4
import config
from kernel import generate
from kernel.sandbox import TSandbox
from kernel.thread_pool import SThreadPool


class TTestingTask:
    def __init__(self, code, options, tests, verifier, response):
        self.status = 'added'
        self.code = code
        self.verifier = verifier
        self.options = options
        self.tests = tests
        self.response = response
        # generate a token
        self.number = str(uuid4())
        self.result = {}

    def start(self, callback):
        self.callback = callback
        SThreadPool().add(self.execute, ())

    def execute(self):
        try:
            sb = TSandbox(self.number)
            res = sb.compile_untrusted(self.code, self.options)
            if 'error' in res:
                self.status = 'failed'
                self.result = res['error']
                return
            self.status = 'compiled'
            gen = generate.TGenerator(self.tests)
            self.status = 'run'
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
            self.callback(self)
        except Exception as e:
            self.status = 'failed'
            self.result = str(e)
            self.callback(self)

    def testing(self, sandbox, generator):
        for test in generator.generate():
            result = {'input': test}
            res = sandbox.execute_untrusted(test)
            if 'error' in res:
                self.status = 'failed'
                self.result = res['error']
                yield result
            else:
                result['output'] = sandbox.get_execution_result()
                res = sandbox.verify_untrusted(self.verifier, test)
                if 'error' in res:
                    self.status = 'failed'
                    self.result = res['error']
                    yield result
                else:
                    result['status'] = res
                    yield result
