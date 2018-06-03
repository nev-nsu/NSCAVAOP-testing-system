from uuid import uuid4
import config
from kernel import generate
from kernel.sandbox import TSandbox
from kernel.thread_pool import SThreadPool


class TTestingTask:
    def __init__(self, code, options, tests, verifier, response):
        print ('DEBUG', code, options, tests, verifier, response)
        self.status = 'added'
        self.code = code
        self.verifier = verifier
        self.options = options
        self.tests = tests
        self.response = response
        # generate a token
        self.number = str(uuid4())
        self.result = {}
        self.callbacks = []

    def start(self):
        SThreadPool().add(self.execute, ())

    def add_cb(self, callback):
        status = self.status
        if status not in ('finished', 'failed'):
            self.callbacks.append(callback)
        else:
            callback(self)

    def execute(self):
        print (self.response)
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
                status = result['status']
                if self.response == 'statistics':
                    if status not in self.result:
                        self.result[status] = 1
                    else:
                        self.result[status] += 1
                elif self.response == 'raw_data' or result['status'] != 'OK':
                    self.result.append(result)
            self.status = 'finished'
            for cb in self.callbacks: cb(self)
        except Exception as e:
            self.status = 'failed'
            self.result = str(e)
            for cb in self.callbacks: cb(self)

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
