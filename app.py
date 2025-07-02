from flask import Flask, request, render_template
import os
import re
import base64

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        level = request.form.get('level')
        regex = request.form.get('regex')

        # 驗證關卡
        if not level or not level.isdigit() or not (1 <= int(level) <= 7):
            result = {'error': '關卡請輸入 1 到 7！'}
            return render_template('index.html', result=result)

        level = int(level)
        accept_path = f'testcase/{level}.accept'
        reject_path = f'testcase/{level}.reject'

        try:
            pattern = re.compile(f"^{regex}$")
        except re.error as e:
            result = {'error': f'無效的正則表達式：{e}'}
            return render_template('index.html', result=result)

        # 讀測資
        def load_lines(path):
            with open(path, encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]

        accept_lines = load_lines(accept_path)
        reject_lines = load_lines(reject_path)

        for line in accept_lines:
            if not pattern.fullmatch(line):
                return render_template('index.html', result={
                    'error': f'❌ Failed accept testcase（該匹配卻沒匹配到）: {line}'
                })

        for line in reject_lines:
            if pattern.fullmatch(line):
                return render_template('index.html', result={
                    'error': f'❌ Failed reject testcase（不該匹配卻匹配到）: {line}'
                })

        keyword = None
        if level == 2:
            keyword = base64.b64decode("aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUTR3NHc5V2djUQ==").decode()
        if level == 3:
            keyword = base64.b64decode("aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUTR3NHc5V2djUQ==").decode()            

        result = {
            'success': True,
            'level': level,
            'keyword': keyword
        }

    return render_template('index.html', result=result)
