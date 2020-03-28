import os
# MeCabリソースファイルへのパスを通す
# MLAsk の使用のために必要
os.environ['MECABRC'] = r'.\venv\Scripts\etc\mecabrc'

from mlask import MLAsk
import re
import spacy
import emotion_db
import decimal

# 各感情を表すテキスト配列
EMOTION_KEYS = ['yorokobi', 'ikari', 'aware', 'kowa', 'haji', 'suki', 'iya', 'takaburi', 'yasu', 'odoroki']

def calc_emotion_score(text):
    """テキストから感情スコアを取得する
    """

    # 感情解析 MLAsk
    emotion_analyzer = MLAsk()
    # 感情を表す単語からカテゴリを取得できる辞書
    emotion_dict = emotion_db.load_emotion_dict()
    # カテゴリから感情スコアを取得できる辞書
    emotion_score_dict = emotion_db.create_emotion_score_dict()

    # スコアを 0 で初期化
    scores = {}
    for key in EMOTION_KEYS:
        scores[key] = 0.0

    # テキストを分割する
    # 半角と全角の句読点と改行を基準に分割
    text_list = re.findall(r'[^(。|、|,|.|\n)]+(?:[(。|、|,|.|\n)]|$)', text)

    # 最初に MLAsk によるスコア付けを行う
    for txt in text_list:
        result = emotion_analyzer.analyze(txt)
        if (result['emotion'] != None):
            for v in result['emotion']:
                # 単純に出てきたスコアに足し算していく
                # intension （感嘆符や顔文字などで増える値）を単純に足すと
                # 正規化した際に他の値が小さくなりすぎるので、いったん係数をかけておく
                scores[v] = scores.get(v, 0) + 1 + (result['intension'] * 0.1)

    # 次に GiNZA による解析を行う
    nlp = spacy.load('ja_ginza')
    for txt in text_list:
        ginza_result = {}
        doc = nlp(txt)
        for sent in doc.sents:
            for token in sent:
                ginza_result[token.i] = token
                # 抜き出した単語が感情スコア付け辞書に存在するか
                if emotion_dict.get(token.lemma_) != None:
                    # 抜き出した単語は感情スコア付け辞書に存在していたが
                    # 否定文なしで使われているかをチェックする
                    if (_is_not_s(doc, token.lemma_ ) == True):
                        continue
                    # 単語は複数のカテゴリに設定されている場合がある
                    for key in emotion_dict.get(token.lemma_):
                        raw_score = emotion_score_dict.get(key)
                        if raw_score != None:
                            for i, v in enumerate(EMOTION_KEYS):
                                scores[v] = scores.get(v, 0) + float(raw_score[i])

    # スコアの最大値を求める
    max_emotion_value, max_emotion_keys = get_max_emotion_score(scores)
    # 最大値が見つかった場合には正規化
    if (len(max_emotion_keys) > 0):
        for key in EMOTION_KEYS:
            scores[key] = _float_quantize(scores[key] / max_emotion_value)
    return scores

def get_max_emotion_score(scores):
    """感情スコアの最大値を取得する

    Returns:
        number: 感情スコアの最大値
        array: 最大の感情スコアを持つキー配列
    """
    max_emotion_keys = []
    max_emotion_value = 0
    for key in scores:
        if (scores[key] > max_emotion_value):
            max_emotion_keys = []
            max_emotion_keys.append(key)
            max_emotion_value = scores[key]
        elif (max_emotion_value > 0 and scores[key] == max_emotion_value):
            max_emotion_keys.append(key)
    return max_emotion_value, max_emotion_keys

def _is_not_s(doc, word):
    """係り受け情報から否定文になっているかを簡易的に判定
    
    Returns:
        bool: 否定文になっている場合 True
    """
    for sent in doc.sents:
        for token in sent:
            if token.lemma_ == "無い" or token.lemma_ == "ない":
                if token.head.text == word:
                    return True
    return False

def _is_not(result, word):
    """係り受け情報から指定された単語が否定されているかを判定
    
    Returns:
        bool: 否定されている場合 True
    """
    for key in result:
        token = result[key]
        # "ない" という文字を見つけた
        if token.lemma_ == "無い" or token.lemma_ == "ない":
            check_token = token
            # チェック対象が最上位になるまでチェックを繰り返す
            while (check_token.i != check_token.head.i):
                # 係り受けの対象に指定された単語が見つかった
                if check_token.head.text == word:
                    return True
                # 上位の係り受け対象に入れ替える
                else:
                    check_token = result[check_token.head.i]
    return False

def _float_quantize(value):
    """少数の切り捨て
    """
    return float(decimal.Decimal(value).quantize(decimal.Decimal('.001'), rounding=decimal.ROUND_DOWN))

#print (calc_emotion_score("彼のことが嫌いではない"))
#text = "メロスは激怒した。必ず、かの邪智暴虐の王を除かなければならぬと決意した。メロスには政治がわからぬ。メロスは、村の牧人である。笛を吹き、羊と遊んで暮して来た。けれども邪悪に対しては、人一倍に敏感であった。"
#print (calc_emotion_score(text))
