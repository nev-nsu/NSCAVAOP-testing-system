import os
import config

def compile_options2string(options):
    res = ''
    if 'optimization_level' in options:
        res += '-O' + options['optimization_level'] + ' '
    return res

class Sandbox:
    def __init__(self, token):
        self.token = token
        self.has_executable = False
        self.has_output = False
        self.dir = config.TEMP_DIR + '/.' + token
        text = 'noblacklist ' + self.dir + '\n' + \
               'whitelist ' + self.dir + '\n' + \
               'include ' + config.SANDBOX_PROFILE + '\n'
        if not os.path.exists(self.dir):
            os.mkdir(self.dir)
        self.profile = os.path.join(self.dir, 'generated.profile')
        f = open(self.profile, 'w')
        f.write(text)
        f.close()

    def verify_untrusted(self, verifier, input_text):
        with open(self.dir + '/verifier.py', 'w') as f:
            f.write(verifier) 
        command = '\'echo "' + input_text + '" | ' 'python ' + self.dir + '/verifier.py' + '>'+self.dir+'/verify_result\''
        all = 'firejail --timeout=0:0:10 --quiet --profile='+self.profile+ ' bash -c ' + command
        os.system(all)
        try:
            with open(self.dir + '/verify_result', 'r') as f:
                res = f.read()
                return res
        except FileNotFoundError:
            return { 'error': 'Internal error at verifier run' }

    def execute_untrusted(self, input_text):
        if self.has_executable == False:
            return { 'error' : 'Executable not found' }
        command = '\'echo "' + input_text + '" | ' + self.dir + '/executable >'+self.dir+'/output\''
        all = 'firejail --timeout=0:0:10 --quiet --profile='+self.profile+ ' bash -c ' + command
        os.system(all)
        self.has_output = True
        # check
        return {}

    def compile_untrusted(self, code, options):
        # change to c++
        command = '\' echo "' + code + '" | gcc -x c - -o ' + self.dir + '/executable ' + \
                compile_options2string(options) +'\''
        args = ['firejail', '--timeout=0:0:10', '--profile='+self.profile, 'bash', '-c', command]
        all = 'firejail --timeout=0:0:10 --profile='+self.profile+ ' bash -c ' + command
        os.system(all)
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

