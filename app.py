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
        if level == 1:
            keyword = base64.b64decode("ZmxhZ+eahOmghuW6j+aYr+esrDLpoYzihpLnrKw06aGM4oaS56ysNumhjOKGkuesrDfpoYzihpLnrKw16aGM4oaS56ysM+mhjA==").decode()
        elif level == 2:
            keyword = base64.b64decode("RkxBR3s2UjM0Nyxf").decode()
        elif level == 3:
            keyword = base64.b64decode("NTE3QzBOX0M0TVAufQ==").decode()   
        elif level == 4:
            keyword = base64.b64decode("WTBVX0g0VjNf").decode()   
        elif level == 5:
            keyword = base64.b64decode("VzNMQzBNM183MF8=").decode()   
        elif level == 6:
            keyword = base64.b64decode("MTM0Uk4zRF9IMFdfNzBf").decode()   
        elif level == 7:
            keyword = base64.b64decode("VTUzX1IzNjNYO18=").decode()   

        result = {
            'success': True,
            'level': level,
            'keyword': keyword
        }

    return render_template('index.html', result=result)
@app.route('/describe/<int:level>')
def describe(level):
    if 1 <= level <= 7:
        path = f'describe/{level}.txt'
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                return jsonify({'text': f.read()})
        else:
            return jsonify({'text': '(尚未提供描述)'})
    return jsonify({'text': '❌ 關卡編號錯誤'})

