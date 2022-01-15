# -*- coding: utf-8 -*-

import requests
import re
from tqdm import tqdm
from multiprocessing.pool import ThreadPool



def link_TagMe_db(concept):
    try:
        concept = re.sub(r'http\S+', '', concept)
        #print(concept)
        url="https://tagme.d4science.org/tagme/tag?lang=en&gcube-token=bbcf7be9-ad39-487c-9872-6b1bbc77baf1-843339462&text="+concept
        response = requests.post(url)
        if response.status_code != 200:
            return -1
        results=response.json()
        #print(results)
        entities=[]  
        for result in results["annotations"]:
            try:
                if result['link_probability']>=0.30:
                    entities.append(result["spot"]+":"+result["title"].replace(" ","_"))
            except:
                continue
        return entities
    except:
        return -1
    
    
    
    
import csv


filename="../data/TweetsCOV19_052020/TweetsCOV19_052020_ids_text.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)
    
    
tweets_text=dict()    
for row in rows[1:]:
    tweets_text[row[6]]=row[17]


filename="../data/TweetsCOV19_052020/TweetsCOV19_ids_entities_db_org.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)
    


global final_tweets
final_tweets=[]    

def get_entities(row):
    global counter
    print(counter)
    counter+=1
    global final_tweets
    temp_list_uris=[]
    entities_tagme=[]
    tweet_entities_final=''
    if row[0] in tweets_text:
        entities_tagme=link_TagMe_db(tweets_text[row[0]])
    if entities_tagme==-1:
        tweet_entities_final=row[1]
    else:
        tweet_entities_final=row[1]
        tweet_entities=row[1].split(';')[:-1]
        for entity in tweet_entities:
            entity=entity.split(":")
            entity_uri=entity[1]
            temp_list_uris.append(entity_uri)
        for entity in entities_tagme:
            entity=entity.split(":")
            entity_uri=entity[1]
            entity_label=entity[0]
            if entity_uri not in temp_list_uris:
                tweet_entities_final+=entity_label+':'+entity_uri+";"
    final_tweets.append([row[0].strip(),tweet_entities_final])


    
global counter                
counter=0

pool = ThreadPool(12)
pool.map(get_entities, rows)
pool.close()
pool.join()


                
with open("../data/TweetsCOV19_052020/TweetsCOV19_ids_entities_db_combined.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        writer.writerows(final_tweets)
            
                
                
        
        