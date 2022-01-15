# -*- coding: utf-8 -*-



from gensim.models import Word2Vec



wv_from_text = Word2Vec.load('embedding/data/wikidata/wikidata-20170613')



def get_similarity(e1,e2):
    if e1 in wv_from_text.wv.vocab and e2 in wv_from_text.wv.vocab:
        return wv_from_text.wv.similarity(e1,e2)
    else:
        return 0






