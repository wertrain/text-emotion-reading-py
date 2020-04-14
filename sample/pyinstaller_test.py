import spacy
import sys
import os
# MeCabリソースファイルへのパスを通す
# MLAsk の使用のために必要
os.environ['MECABRC'] = r'.\etc\mecabrc'

nlp = spacy.load('ja_ginza')
doc = nlp('彼のことが嫌いではなかった')

print (doc)


