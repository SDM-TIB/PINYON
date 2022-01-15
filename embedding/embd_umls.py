# -*- coding: utf-8 -*-

import csv
from scipy import spatial


filename="embedding/data/umls/cui2vec_pretrained.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)
    

rows.pop(0)    
umls_vec=dict()


dataSetI=[float(x) for x in rows[1][1:]]
dataSetII=[float(x) for x in rows[2][1:]]
result = 1 - spatial.distance.cosine(dataSetI, dataSetII)


for row in rows:
    umls_vec[row[0]]=[float(x) for x in row[1:]]
    
    
    

def get_similarity(e1,e2):
    if e1 in umls_vec and e2 in umls_vec:
        return 1 - spatial.distance.cosine(umls_vec[e1], umls_vec[e2])
    else:
        return 0