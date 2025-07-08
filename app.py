
from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = 'your-secret-key'

@app.route('/', methods=['GET', 'POST'])
def choose_team():
    if request.method == 'POST':
        team = request.form.get('team')
        if team and team.isdigit() and 0 <= int(team) <= 9:
            session['team'] = int(team)
            return redirect(url_for('start_game'))
        else:
            return render_template('choose_team.html', error="請選擇 0 到 9 的小隊")
    return render_template('choose_team.html')

@app.route('/start_game')
def start_game():
    team = session.get('team')
    if team is None:
        return redirect(url_for('choose_team'))
    return render_template('game.html', team=team)

if __name__ == '__main__':
    app.run(debug=True)
