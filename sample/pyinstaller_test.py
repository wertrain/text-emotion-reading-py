import spacy
import sys
sys.path.append('../')

nlp = spacy.load('ja_ginza')
doc = nlp('彼のことが嫌いではなかった')


