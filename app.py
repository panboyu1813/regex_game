from flask import Flask, render_template, request
import re
import os

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        regex = request.form['regex']
        try:
            pattern = re.compile(regex)
        except re.error as e:
            result = { 'error': f'無效的正則表達式：{e}' }
            return render_template('index.html', result=result)

        def load_lines(filename):
            path = os.path.join('testcase', filename)
            with open(path, 'r', encoding='utf-8') as f:
                return [line.strip() for line in f.readlines()]

        accept_cases = load_lines('accept1.txt')
        reject_cases = load_lines('reject1.txt')

        passed_accept = sum(1 for s in accept_cases if pattern.fullmatch(s))
        failed_accept = len(accept_cases) - passed_accept

        passed_reject = sum(1 for s in reject_cases if pattern.fullmatch(s))
        correct_reject = len(reject_cases) - passed_reject

        result = {
            'passed_accept': passed_accept,
            'total_accept': len(accept_cases),
            'failed_accept': failed_accept,
            'passed_reject': passed_reject,
            'total_reject': len(reject_cases),
            'correct_reject': correct_reject
        }

    return render_template('index.html', result=result)
