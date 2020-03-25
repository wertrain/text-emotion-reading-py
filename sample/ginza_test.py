import spacy
import sys
sys.path.append('../')

nlp = spacy.load('ja_ginza')
doc = nlp('彼のことが嫌いではない')

###依存構文解析結果の表形式表示
result_list = []
for sent in doc.sents:
    for token in sent:
      #コメントは公式サイト記載ではなく、解釈なので参考程度に。
      info_dict = {}
      info_dict[".i"]             = token.i             # トークン番号（複数文がある場合でも0に戻らず連番になる）
      info_dict[".orth_"]         = token.orth_         # オリジナルテキスト
      info_dict["._.reading"]     = token._.reading     # 読み仮名
      info_dict[".pos_"]          = token.pos_          # 品詞(UD)
      info_dict[".tag_"]          = token.tag_          # 品詞(日本語)
      info_dict[".lemma_"]        = token.lemma_        # 基本形（名寄せ後）
      info_dict["._.inf"]         = token._.inf         # 活用情報
      info_dict[".rank"]          = token.rank          # 頻度のように扱えるかも
      info_dict[".norm_"]         = token.norm_         # 原型
      info_dict[".is_oov"]        = token.is_oov        # 登録されていない単語か？
      info_dict[".is_stop"]       = token.is_stop       # ストップワードか？
      info_dict[".has_vector"]    = token.has_vector    # word2vecの情報を持っているか？
      info_dict["list(.lefts)"]   = list(token.lefts)   # 関連語まとめ(左)
      info_dict["list(.rights)"]  = list(token.rights)  # 関連語まとめ(右)
      info_dict[".dep_"]          = token.dep_          # 係り受けの関係性
      info_dict[".head.i"]        = token.head.i        # 係り受けの相手トークン番号
      info_dict[".head.text"]     = token.head.text     # 係り受けの相手のテキスト
      result_list.append(info_dict)

#import pprint
#pprint.pprint (result_list)

emotion_dict = {}
emotion_dict["嫌い"] = [0,0,0]

for sent in doc.sents:
    for token in sent:
      if emotion_dict.get(token.lemma_) != None:
          for key in emotion_dict.get(token.lemma_):
              print (key)