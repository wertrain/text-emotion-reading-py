import os
os.environ['MECABRC'] = r'.\venv\Scripts\etc\mecabrc'

import logging
from flask import Flask, render_template, request, url_for
from mlask import MLAsk
import re
import spacy
import emotion_db

app = Flask(__name__)
emotion_analyzer = MLAsk()
emotion_dict = emotion_db.load_emotion_dict()
emotion_score_dict = emotion_db.create_emotion_score_dict()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/form')
def form():
    return render_template('form.html')

@app.route('/analysis', methods=['POST'])
def analysis():
    text = request.form['text']
    text_list = re.findall(r'[^(。|、|,|.|\n)]+(?:[(。|、|,|.|\n)]|$)', text)

    analyzed = {}
    emotion_keys = ['yorokobi', 'ikari', 'aware', 'kowa', 'haji', 'suki', 'iya', 'takaburi', 'yasu', 'odoroki']
    emotion_emoji_map = {
        'yorokobi':'smile', 'ikari':'angry', 'aware':'cry', 'kowa':'fearful', 'haji':'flushed', 
        'suki':'heart_eyes', 'iya':'confounded', 'takaburi':'triumph', 'yasu':'relaxed', 'yasu':'open_mouth'
    }
    not_emotion_emoji = 'expressionless'
    emotion_jpn_map = {
        'yorokobi':'喜び', 'ikari':'怒り', 'aware':'哀しい', 'kowa':'怖い', 'haji':'恥', 
        'suki':'好き', 'iya':'厭', 'takaburi':'昂ぶり', 'yasu':'安らぎ', 'yasu':'驚き'
    }

    for emo in emotion_keys:
        analyzed[emo] = 0.0
    for txt in text_list:
        result = emotion_analyzer.analyze(txt)
        if (result['emotion'] != None):
            for v in result['emotion']:
                analyzed[v] = analyzed.get(v, 0) + 1 + result['intension']

    nlp = spacy.load('ja_ginza')
    for txt in text_list:
        doc = nlp(txt)
        for sent in doc.sents:
            for token in sent:
                if emotion_dict.get(token.lemma_) != None:
                    for key in emotion_dict.get(token.lemma_):
                        score = emotion_score_dict.get(key)
                        if score != None:
                            for i, v in enumerate(emotion_keys):
                                analyzed[v] = analyzed.get(v, 0) + float(score[i])

    max_emotion_key = ''
    max_emotion_value = 0
    for data in analyzed:
        if (analyzed[data] > max_emotion_value):
            max_emotion_key = data
            max_emotion_value = analyzed[data]
    
    icon = not_emotion_emoji
    overview = '感情が読み取れない文章です'
    if (len(max_emotion_key) > 0):
        icon = emotion_emoji_map[max_emotion_key]
        overview = '「' + emotion_jpn_map[max_emotion_key] + '」の感情が強い文章です'
        # 最大値が見つかった場合には底上げ＆正規化
        for emo in emotion_keys:
            if analyzed[emo] == 0:
                analyzed[emo] = analyzed[emo] + 0.1
            else:
                analyzed[emo] = analyzed[emo] / max_emotion_value

    return render_template(
        'analysis.html',
        text=text,
        result=analyzed,
        overview=overview,
        icon=icon)

@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500

@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

if __name__ == "__main__":
    app.run(debug=True)
