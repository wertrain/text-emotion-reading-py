from mlask import MLAsk
import pprint

emotion_analyzer = MLAsk()
result = emotion_analyzer.analyze('彼のことは嫌いではない！(;´Д`)')

pprint.pprint (result)