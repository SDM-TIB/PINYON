# -*- coding: utf-8 -*-

import csv

filename="data/TweetsCOV19_052020/all_entities.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    all_entities=list(reader)
 
    
filename="data/TweetsCOV19_052020/tweets.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    tweets=list(reader)   
    
filename="data/TweetsCOV19_052020/TweetsCOV19_052020_ids_text.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    tweets_text=list(reader) 
    
    
tweets_text.pop(0)    
post_2_text_dict=dict()

for post in tweets_text:
    post_2_text_dict[post[6]]=post[17]
    

    
entity_post_dict=dict()

for tweet in tweets:
    tweet_entities=tweet[1]
    tweet_id=tweet[0]
    for entity in tweet_entities.split(';'):
        if entity not in entity_post_dict:
            entity_post_dict[entity]=[]
        entity_post_dict[entity].append(tweet_id)
        
        
        
entity_id_2_mention_db=dict()
entity_id_2_mention_wiki=dict()
entity_id_2_mention_umls=dict()

for row in all_entities:
    mention=row[0]
    entity_db=row[1]
    entity_wiki=row[2]
    entity_umls=row[3]
    
    
    if entity_db!="":
        if entity_db not in entity_id_2_mention_db:
            entity_id_2_mention_db[entity_db]=[]
        entity_id_2_mention_db[entity_db].append(mention)
    
    if entity_wiki!="":
        if entity_wiki not in entity_id_2_mention_wiki:
            entity_id_2_mention_wiki[entity_wiki]=[]
        entity_id_2_mention_wiki[entity_wiki].append(mention)
               
    if entity_umls!="":
        if entity_umls not in entity_id_2_mention_umls:
            entity_id_2_mention_umls[entity_umls]=[]
        entity_id_2_mention_umls[entity_umls].append(mention)
    

def edge_2_mention(edge,kg):
    edge=edge.split(';')
    e2=edge[1]
    
    if kg=='wiki':
        if e2 in entity_id_2_mention_wiki:
            return entity_id_2_mention_wiki[e2]
        else:
            return ""
    elif kg=='umls':
        if e2 in entity_id_2_mention_umls:
            return entity_id_2_mention_umls[e2]
        else:
            return ""
    else:
        if e2 in entity_id_2_mention_db:
            return entity_id_2_mention_db[e2]
        else:
            return ""
    
    
def mention_2_post(mention):
    if mention in entity_post_dict:
        return entity_post_dict[mention]
    else:
        return ""

def post_2_text(post):
    if post in post_2_text_dict:
        return post_2_text_dict[post]
    else:
        return ""
    
    
            