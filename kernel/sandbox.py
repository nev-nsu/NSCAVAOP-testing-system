import os
from config import SConfig


def compile_options2string(options):
    res = ''
    if 'optimization_level' in options:
        res += '-O' + options['optimization_level'] + ' '
    return res


class TSandbox:
    def __init__(self, token):
        self.token = token
        self.has_executable = False
        self.has_output = False
        self.dir = SConfig().TEMP_DIR + '/.' + token
        text = 'noblacklist ' + self.dir + '\n' + \
               'whitelist ' + self.dir + '\n' + \
               'include ' + SConfig().SANDBOX_PROFILE + '\n'
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.profile = os.path.join(self.dir, 'generated.profile')
        f = open(self.profile, 'w')
        f.write(text)
        f.close()

    def verify_untrusted(self, verifier, input_text):
        with open(self.dir + '/verifier.py', 'w') as f:
            f.write(verifier)
        command = '\'echo "' + input_text + '" | ' 'python ' + \
            self.dir + '/verifier.py' + '>' + self.dir + '/verify_result\''
        full_command = 'firejail --timeout=0:0:10 --quiet --profile=' + \
            self.profile + ' bash -c ' + command
        os.system(full_command)
        try:
            with open(self.dir + '/verify_result', 'r') as f:
                res = f.read()
                return res
        except FileNotFoundError:
            return {'error': 'Internal error at verifier run'}

    def execute_untrusted(self, input_text):
        if not self.has_executable:
            return {'error': 'Executable not found'}
        command = '\'echo "' + input_text + '" | ' + \
            self.dir + '/executable >' + self.dir + '/output\''
        full_command = 'firejail --timeout=0:0:10 --quiet --profile=' + \
            self.profile + ' bash -c ' + command
        os.system(full_command)
        self.has_output = True
        # check
        return {}

    def compile_untrusted(self, code, options):
        with open(self.dir + '/main.cpp', 'w') as f:
            f.write(code)
        command = '\'g++ '+ self.dir + '/main.cpp -o ' + self.dir + \
            '/executable ' + compile_options2string(options) + '\''
        full_command = 'firejail --timeout=0:0:10 --quiet --profile=' + \
            self.profile + ' bash -c ' + command
        print('execute:', command)
        os.system(full_command)
        self.has_executable = True
        # check result of execution
        return {}

    def get_execution_result(self):
        assert self.has_output
        if not hasattr(self, 'output'):
            try:
                with open(self.dir + '/output', 'r') as f:
                    res = f.read()
                    self.output = res
            except FileNotFoundError:
                self.output = ''
        return self.output
