from janome.tokenizer import Tokenizer

t = Tokenizer()
s = '''
新しい人達に接して見ても、一週間たつかたたない内に、彼は又しても底知れぬ倦怠けんたいの中に沈み込んで了うのでした。
そうして、東栄館に移って十日ばかりたったある日のことです。退屈の余り、彼はふと妙な事を考えつきました。
'''
for token in t.tokenize(s):
    print(token)
