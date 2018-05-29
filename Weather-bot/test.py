import spacy
import difflib


nlp = spacy.load('es')  # make sure to use larger model!
tokens = nlp(u'Mujer Majer Mijar Carro')

for token1 in tokens:
    for token2 in tokens:
        print(token1.text, token2.text, token1.similarity(token2))
        print(difflib.SequenceMatcher(None, token1.text.lower(), token2.text.lower()).ratio())
