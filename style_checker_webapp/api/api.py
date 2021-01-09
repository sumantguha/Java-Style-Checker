import importlib
import importlib.util
import json
import subprocess
import sys

try:
    from flask import Flask, request
except ImportError:
    subprocess.check_call([sys.executable, "-m", "pip", "install", 'flask'])

try:
    from flask_cors import CORS
except ImportError:
    subprocess.check_call(
        [sys.executable, "-m", "pip", "install", 'flask_cors'])


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = module_from_file(
    '*', '../../style_checker_modular.py')

app = Flask(__name__)
CORS(app)


class SetEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, set):
            return list(obj)
        return json.JSONEncoder.default(self, obj)


@app.route('/code', methods=['GET', 'POST'])
def result():
    if request.json:
        content = request.json
        print(content)
        with open('student_file.java', 'w') as file:
            file.write(str(content['code']))
        tests = checker.main('student_file.java',
                             mode='web', verbose=True, debug=True, tabsize=int(content['tabsize']))
        return json.dumps(tests, cls=SetEncoder)
    return "No code"
