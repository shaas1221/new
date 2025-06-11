from flask import Flask, render_template, request
import json
import random
import re

app = Flask(__name__)

# تحميل العبارات من JSON
with open('sentences.json', encoding='utf-8') as f:
    SENTENCES = json.load(f)

# تطبيع الإجابة (إزالة علامات الترقيم والمسافات الزائدة)
def normalize(text):
    return re.sub(r'\s+', ' ', re.sub(r'[^\w\s]', '', text)).strip()

@app.route('/', methods=['GET'])
def start_game():
    # اختيار نمط عشوائي: ترتيب أو اختيار
    game_type = random.choice(['arrange', 'choose'])
    return render_game(game_type)

def render_game(game_type):
    sentence = random.choice(SENTENCES)
    if game_type == 'arrange':
        words = sentence['phrase'].split()
        random.shuffle(words)
        return render_template('index.html',
                               reference=sentence['reference'],
                               words=words,
                               correct_answer=sentence['phrase'],
                               game_type='arrange')
    else:
        choices = sentence['choices']
        random.shuffle(choices)
        return render_template('choose.html',
                               phrase=sentence['phrase'],
                               choices=choices,
                               correct_answer=sentence['reference'],
                               game_type='choose')

@app.route('/submit', methods=['POST'])
def submit():
    game_type = request.form['game_type']
    user_answer = normalize(request.form['user_answer'])
    correct_answer = normalize(request.form['correct_answer'])
    is_correct = user_answer == correct_answer
    return render_template('result.html',
                           correct=is_correct,
                           correct_answer=correct_answer)

if __name__ == '__main__':
    app.run(debug=True)
