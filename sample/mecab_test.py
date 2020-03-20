import os
os.environ['MECABRC'] = r'.\venv\Scripts\etc\mecabrc'

import MeCab
mecab = MeCab.Tagger ("-Ochasen")
print(mecab.parse("すもももももももものうち"))
