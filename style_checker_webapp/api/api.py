from flask import Flask, request, jsonify
from flask_cors import CORS
import importlib
import importlib.util


def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


checker = module_from_file(
    '*', '../../style_checker_modular.py')

app = Flask(__name__)
CORS(app)


@app.route('/code', methods=['GET', 'POST'])
def result():
    if request.json:
        content = request.json
        with open('student_file.java', 'w') as file:
            file.write(str(content))
        tests = checker.main('student_file.java',
                             mode='web', verbose=True, debug=False)
        return jsonify(result=str(tests))
    return "No code"
