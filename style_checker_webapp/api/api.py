from flask import Flask, request
from flask_cors import CORS
import importlib
import importlib.util
import json


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
        with open('student_file.java', 'w') as file:
            file.write(str(content))
        tests = checker.main('student_file.java',
                             mode='web', verbose=True, debug=False)

        return json.dumps(tests, cls=SetEncoder)
    return "No code"
