# -*- coding: utf-8 -*-


import csv
from tqdm import tqdm
from embedding import embd_db
import graph
from PINYON_scd import scd
from tweets_process import tweets_helper

def edge_similarity(e1,e2):
    n1_entities=e1.split(';')
    n1_start=n1_entities[0]
    n1_end=n1_entities[1]
    n2_entities=e2.split(';')
    n2_start=n2_entities[0]
    n2_end=n2_entities[1]
    
    
    similarity=0
    temp=embd_db.get_similarity(n1_start,n1_end)
    if temp >0:
        similarity+=temp
    temp=embd_db.get_similarity(n1_start,n2_start)
    if temp >0:
        similarity+=temp
    temp=embd_db.get_similarity(n1_start,n2_end)
    if temp >0:
        similarity+=temp
    temp=embd_db.get_similarity(n1_end,n2_start)
    if temp >0:
        similarity+=temp
    temp=embd_db.get_similarity(n1_end,n2_end)
    if temp >0:
        similarity+=temp
    temp=embd_db.get_similarity(n2_start,n2_end)
    if temp >0:
        similarity+=temp


    similarity=similarity/6
    
    return similarity


filename="data/TweetsCOV19_052020/entities_db.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows_db=list(reader)


db_entities=dict()
for row in rows_db:
    db_entities[row[1]]=row[0]
    
    
    
    
all_entities=[]

all_entities.extend([x[1] for x in rows_db[:]])

post_entities=['Neoadjuvant_therapy','Nivolumab','Non-small-cell_lung_carcinoma','Phases_of_clinical_research']



nodes=[]

for e in post_entities:
    for e_c in all_entities:
        nodes.append(e+';'+e_c)



nodes=list(set(nodes))
complement_graph=graph.graph()  
similarity_max=0
for i in tqdm(range(len(nodes))):
    for j in range(len(nodes)):
        
        if j<i:
            continue
        
        if i==j:
            continue
        
        
        
        n1_entities=nodes[i].split(';')
        n1_start=n1_entities[0]
        n1_end=n1_entities[1]
        n2_entities=nodes[j].split(';')
        n2_start=n2_entities[0]
        n2_end=n2_entities[1]
        
  

        similarity=edge_similarity(nodes[i],nodes[j])
        
        if similarity > similarity_max:
            similarity_max=similarity
        
            
        if n1_start!=n2_start and n1_end!=n2_end:
            complement_graph.append(nodes[i],nodes[j],0)
        else:
            if similarity<0.50:
                complement_graph.append(nodes[i],nodes[j],0)




vertex_coloring=scd(complement_graph)
unique_colors=dict()
for key,value in vertex_coloring.items():
    if value not in unique_colors:
        unique_colors[value]=[]
    unique_colors[value].append(key)
    
 
colors_similarity=dict()       
for key,value in unique_colors.items():
    community_similarity=0
    counter=0
    for i in range(len(value)):
        for j in range(i,len(value)):
            if i==j:
                continue
            community_similarity+=edge_similarity(value[i],value[j])
            counter+=1
    if len(value)==1:
        community_similarity=edge_similarity(value[0],value[0])
    else:
        community_similarity=community_similarity/counter
    colors_similarity[key]=community_similarity
        
    
community_similarity_ordered=sorted(colors_similarity.items(), key=lambda x: x[1], reverse=True)

returned_posts=dict()

for community in community_similarity_ordered:
    if community[1]>0.50:
        for edge in unique_colors[community[0]]:
            mentions=tweets_helper.edge_2_mention(edge,'db')
            if mentions!="":
                for mention in mentions:
                    posts=tweets_helper.mention_2_post(mention)
                    if posts!="":
                        for post in posts:
                            if post not in returned_posts:
                                returned_posts[post]=[]
                            if mention not in returned_posts[post]:
                                returned_posts[post].append(mention)
                            
                        
ranked_posts=sorted(returned_posts, key=lambda k: len(returned_posts[k]), reverse=True)

ranked_posts_text=[]
for post in ranked_posts:
    ranked_posts_text.append(tweets_helper.post_2_text(post))
                
      
