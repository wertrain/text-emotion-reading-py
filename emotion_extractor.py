import argparse
import emotion_score
import os

parser = argparse.ArgumentParser(description='日本語テキストから感情を抽出') 
parser.add_argument('text', help='感情を抽出したいテキスト')
args = parser.parse_args() 

if __name__ == '__main__':
    scores = emotion_score.calc_emotion_score(args.text)
    _, max_emotion_keys = emotion_score.get_max_emotion_score(scores)
    print(scores)
