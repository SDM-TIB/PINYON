# -*- coding: utf-8 -*-

import csv
import requests
from tqdm import tqdm
from multiprocessing.pool import ThreadPool

headers = {'content-type': 'application/json', 'Accept-Charset': 'UTF-8'}


    
def falcon_call_wikidata(text,mode='short'):
    try:
        text=text.replace('"','')
        text=text.replace("'","")
        if mode=='short':
            url = 'https://labs.tib.eu/falcon/falcon2/api?mode=short'
            entities=[]
            payload = '{"text":"'+text+'"}'
            r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
            if r.status_code == 200:
                response=r.json()
                #print(response)
                for result in response['entities']:
                    entities.append(result[0])
            else:
                r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
                if r.status_code == 200:
                    response=r.json()
                    for result in response['entities_wikidata']:
                        entities.append(result[0])
            if len(entities)==0:
                return -1
            return entities[0].replace('<','').replace('>','')
    except:
        return -1        

def getCui(text, mode='short'):
    text=text.replace('"','')
    text=text.replace("'","")
    if mode=='short':
        url = 'https://labs.tib.eu/sdm/biofalcon/api?mode='+mode
        payload = '{"text":"'+text+'"}'
        try:
            r = requests.post(url, data=payload.encode('utf-8'), headers=headers)
            if r.status_code == 200:
                response=r.json()
                if len(response['entities']) > 1:
                    return response['entities'][1][0]
                else:
                    return ""
            else:
                return ""
        except:
            return ""

filename="../data/TweetsCOV19_052020/TweetsCOV19_ids_entities_db_combined.csv"
with open(filename, 'r' , encoding='utf-8') as file:
    reader = csv.reader(file,delimiter=',')
    rows=list(reader)

    
db_entities=dict()
wiki_entities=dict()
UMLS_entities=dict()
all_entities=dict()
tweets=[]

for row in tqdm(rows):
    post_entities=''
    if row[1]=='':
        continue
    for entity_pair in row[1].split(';')[:-1]:
        entity=entity_pair.split(":")
        if len(entity)<2:
            continue
        entity_uri=entity[1]
        entity_label=entity[0]
        post_entities+=entity_label+';'
        if entity_label.lower().strip() not in all_entities:
            all_entities[entity_label.lower().strip()]=''
        if entity_label.lower().strip() not in db_entities:
            db_entities[entity_label.lower().strip()]=entity_uri
        if entity_label.lower().strip() not in wiki_entities:
            entity_uri=falcon_call_wikidata(entity_label.lower().strip().replace('_',' '))
            if entity_uri!=-1:
                wiki_entities[entity_label.lower().strip()]=entity_uri.replace('http://www.wikidata.org/entity/','')
        if entity_label.lower().strip() not in UMLS_entities:
            entity_uri=getCui(entity_label.lower().strip().replace('_',' '))
            if entity_uri!='':
                UMLS_entities[entity_label.lower().strip()]=entity_uri
    tweets.append([row[0],post_entities])
    
    
entities_uris=[]    
for key,value in all_entities.items():
    db_link=''
    wiki_link=''
    umls_link=''
    if key in db_entities:
        db_link=db_entities[key]
    if key in wiki_entities:
        wiki_link=wiki_entities[key]
    if key in UMLS_entities:
        umls_link=UMLS_entities[key]
    entities_uris.append([key,db_link,wiki_link,umls_link])
    
    
with open("../data/TweetsCOV19_052020/tweets.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        writer.writerows(tweets)
        
with open("../data/TweetsCOV19_052020/all_entities.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        writer.writerows(entities_uris)


with open("../data/TweetsCOV19_052020/entities_db.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for key,value in db_entities.items():
            writer.writerow([key,value])
            
with open("../data/TweetsCOV19_052020/entities_wiki.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for key,value in wiki_entities.items():
            writer.writerow([key,value])
            
with open("../data/TweetsCOV19_052020/entities_umls.csv", "w", encoding="utf-8") as output:
        writer = csv.writer(output, delimiter=',', lineterminator='\n')
        for key,value in UMLS_entities.items():
            writer.writerow([key,value])
            
    


                
        
        
    
    
    

