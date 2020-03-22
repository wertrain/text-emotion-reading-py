import os
os.environ['MECABRC'] = r'.\venv\Scripts\etc\mecabrc'

from mlask import MLAsk
import pprint
import re

text='''
メロスは激怒した。必ず、かの邪智暴虐じゃちぼうぎゃくの王を除かなければならぬと決意した。メロスには政治がわからぬ。
'''
emotion_analyzer = MLAsk()
text_list = re.findall(r'[^(。|、|,|.|\n)]+(?:[(。|、|,|.|\n)]|$)', text)

analyzed = {}
emotion = ['yorokobi', 'ikari', 'aware', 'kowa', 'haji', 'suki', 'iya', 'takaburi', 'yasu', 'odoroki']
for emo in emotion:
    analyzed[emo] = 0

for txt in text_list:
    result = emotion_analyzer.analyze(txt)
    print(result)
    if (result['emotion'] != None):
        for v in result['emotion']:
            analyzed[v] = analyzed.get(v, 0) + 1 + result['intension']

pprint.pprint (analyzed)
