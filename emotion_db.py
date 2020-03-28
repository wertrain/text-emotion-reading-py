import xml.etree.ElementTree as ET
import csv
import pickle

def create_emotion_score_dict():
    """カテゴリをキーとした感情スコア辞書を作成する
    
    Returns:
        dictionary: 感情スコア辞書
    """
    score_dict = {}
    with open("emotion_score_asynset.csv", "r") as f:
        data = csv.reader(f)
        next(data)
        for line in data:
            word = line.pop(0)
            score_dict[word] = line
    return score_dict

def create_emotion_dict():
    """感情を表す語をキーとしたカテゴリ辞書を作成する
    
    Returns:
        dictionary: カテゴリ辞書
    """
    tree = ET.parse('jpn-asynset.xml')
    root = tree.getroot()
    emotion_dict = {}
    for syn in root.iter('noun-syn'):
        key = syn.attrib['categ']
        for jpn in syn.iter('jpn-word'):
            lemma = jpn.attrib['lemma']
            if (emotion_dict.get(lemma) == None):
                emotion_dict[lemma] = []
            emotion_dict[lemma].append(key)
    return emotion_dict

def load_emotion_dict():
    """感情を表す語をキーとしたカテゴリ辞書をファイルから読み込む
    """
    with open("emotion_dict.bin", mode='rb') as f:
        data = pickle.load(f)
        return data

def save_emotion_dict():
    """感情を表す語をキーとしたカテゴリ辞書をファイルに出力
    """
    with open("emotion_dict.bin", mode='wb') as f:
        pickle.dump(create_emotion_dict(),f)
