# -*- coding: utf-8 -*-


import csv
from tqdm import tqdm

filename="../data/TweetsCOV19_052020/TweetsCOV19_052020.tsv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter='\t',quoting=csv.QUOTE_NONE)
    rows=list(reader)
    
    
tweets=[]   
tweets_ids=[]
 
for row in tqdm(rows[:50]):
    final_entities=''
    tweet_id=row[0]
    tweets_ids.append(tweet_id)
    tweet_entities=row[7]
    if tweet_entities!='null;':
        tweet_entities=tweet_entities.split(';')[:-1]
        for entity in tweet_entities:
            entity=entity.split(":")
            entity_label=entity[0]
            entity_uri=entity[1]
            final_entities+=entity_label+':'+entity_uri+";"
    tweets.append([tweet_id,final_entities])
    
    
with open("../data/TweetsCOV19_052020/TweetsCOV19_ids_entities_db_org.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        writer.writerows(tweets)
            
        
with open("../data/TweetsCOV19_052020/TweetsCOV19_ids.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for row in tweets_ids:
            writer.writerow([row])