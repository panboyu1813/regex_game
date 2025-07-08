from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from flask import flash
import os
import re
import base64
import requests
from dotenv import load_dotenv

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage?chat_id={TELEGRAM_CHAT_ID}&text={message}"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message
    }
    try:
        response = requests.post(url)
        print("[Telegram Response]", response.status_code, response.text)
    except Exception as e:
        print("[Telegram Error]", e)
    
    except Exception as e:
        print(f"Telegram error: {e}")


load_dotenv()

app = Flask(__name__)
app.secret_key = 'super-secret-key'


@app.route('/select_team', methods=['GET', 'POST'])
def select_team():
    if request.method == 'POST':
        team = request.form.get('team')
        if team in [str(i) for i in range(1, 10)]:
            session['team'] = team
            session['unlocked_level'] = 1
            send_telegram_message(f"第{team}小隊-已開始遊戲")
            return redirect(url_for('index'))
        else:
            flash('請選擇有效的小隊')
    return render_template('select_team.html')

@app.route('/', methods=['GET', 'POST'])
def index():
    if 'team' not in session:
        return redirect(url_for('select_team'))

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
            send_telegram_message(f'小隊{session["team"]} - 嘗試跳關')
            return render_template('index.html', result=result, unlocked_level=unlocked_level, selected_level=level)

        try:
            pattern = re.compile(regex.encode('utf-8').decode('unicode_escape'))
        except re.error as e:
            result = {'error': f'無效的正則表達式：{e}'}
            send_telegram_message(f'小隊{session["team"]} - 已嘗試第{level}關 `{regex}` - 失敗{e}')
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
                # send_telegram_message(f'小隊{session["team"]} - 已嘗試第{level}關 `{regex}` - 失敗')

        for line in reject_lines:
            if pattern.fullmatch(line):
                return render_template('index.html', result={
                    'error': f'❌ Failed reject testcase（不該匹配卻匹配到）: {line}'
                }, unlocked_level=unlocked_level, selected_level=level)
                # send_telegram_message(f'小隊{session["team"]} - 已嘗試第{level}關 `{regex}` - 失敗')

        if level == unlocked_level and level < 10:
            send_telegram_message(f'小隊{session["team"]} - 已嘗試第{level}關 `{regex}` - 成功')
            session['unlocked_level'] += 1
            unlocked_level = session['unlocked_level']
        if level == 10:
            send_telegram_message(f'小隊{session["team"]} - 已完成挑戰')
            
        keyword = None
        
        result = {
            'success': True,
            'level': level,
            'keyword': keyword
        }
        current_level = level + 1 if level + 1 <= unlocked_level else level

    return render_template('index.html', result=result, unlocked_level=unlocked_level, selected_level=current_level)

@app.route('/describe/<int:level>')
def describe(level):
    if 1 <= level <= 10:
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
    session['team'] = ""
    return redirect(url_for('index'))

@app.route("/devtools_opened", methods=["POST"])
def devtools_opened():
    send_telegram_message(f'小隊{session["team"]} - 已開啟開發者工具')
    return "", 204
