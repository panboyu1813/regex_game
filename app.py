from flask import Flask, request, render_template, jsonify, session, redirect, url_for
import os
import re
import base64

app = Flask(__name__)
app.secret_key = 'super-secret-key'

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'unlocked_level' not in session:
        session['unlocked_level'] = 1

    unlocked_level = session['unlocked_level']
    result = None
    current_level = 1

    if request.method == 'POST':
        level = int(request.form.get('level'))
        regex = request.form.get('regex')

        if not (1 <= level <= unlocked_level):
            result = {'error': f'⚠️ 你只能挑戰第 1 到第 {unlocked_level} 關'}
            return render_template('index.html', result=result, unlocked_level=unlocked_level, selected_level=level)

        try:
            pattern = re.compile(f"^{regex}$")
        except re.error as e:
            result = {'error': f'無效的正則表達式：{e}'}
            return render_template('index.html', result=result, unlocked_level=unlocked_level, selected_level=level)

        def load_lines(path):
            with open(path, encoding='utf-8') as f:
                return [line.strip() for line in f if line.strip()]

        accept_lines = load_lines(f'testcase/{level}.accept')
        reject_lines = load_lines(f'testcase/{level}.reject')

        for line in accept_lines:
            if not pattern.fullmatch(line):
                return render_template('index.html', result={
                    'error': f'❌ Failed accept testcase（該匹配卻沒匹配到）: {line}'
                }, unlocked_level=unlocked_level, selected_level=level)

        for line in reject_lines:
            if pattern.fullmatch(line):
                return render_template('index.html', result={
                    'error': f'❌ Failed reject testcase（不該匹配卻匹配到）: {line}'
                }, unlocked_level=unlocked_level, selected_level=level)

        if level == unlocked_level and level < 7:
            session['unlocked_level'] += 1
            unlocked_level = session['unlocked_level']

        keyword = None
        if level >= 2:
            keyword = base64.b64decode("aHR0cHM6Ly93d3cueW91dHViZS5jb20vd2F0Y2g/dj1kUTR3NHc5V2djUQ==").decode()

        result = {
            'success': True,
            'level': level,
            'keyword': keyword
        }
        current_level = level + 1 if level + 1 <= unlocked_level else level

    return render_template('index.html', result=result, unlocked_level=unlocked_level, selected_level=current_level)

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

@app.route('/reset')
def reset():
    session['unlocked_level'] = 1
    return redirect(url_for('index'))
