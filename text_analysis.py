import os
os.environ['MECABRC'] = r'D:\Develop\Python\text_emotion_reading_py\venv\Scripts\etc\mecabrc'

from mlask import MLAsk
emotion_analyzer = MLAsk()
print (emotion_analyzer.analyze('彼のことは嫌いではない！(;´Д`)'))
