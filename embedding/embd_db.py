
from gensim.models import KeyedVectors

wv_from_text = KeyedVectors.load('embedding/data/dbpedia2016/dbpedia_500_4_sg_200')




def get_similarity(e1,e2):
    e1='dbr:'+e1
    e2='dbr:'+e2
    if e1 in wv_from_text.wv.vocab and e2 in wv_from_text.wv.vocab:
        return wv_from_text.wv.similarity(e1,e2)
    else:
        return 0




