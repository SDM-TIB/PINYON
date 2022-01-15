# PINYON

PINYON implements a community detection algorithm that can consider the context and meaning of the entities in a post.
PINYON accurately identifies semantically related posts in various contexts.

# Using PINYON

## Pre-processing
In order to use PINYON first, we need to pre-process the corpus of social media posts (tweets).
The TweetsCOV19(may2020) can be downloaded using this [link](https://zenodo.org/record/4593502/files/TweetsCOV19_052020.tsv.gz?download=1)

After downloading the tweets dataset, we need to execute the three scripts in the tweets_process directory.

Once all the scripts finish executing, we need to obtain the tweets' original text. This can be done using [Hydrator](https://github.com/DocNow/hydrator/releases/download/v0.3.0/Hydrator-Setup-0.3.0.exe)


## Embeddings download

The embedding for each corresponsing KG need to be downladed and placed in embedding/data/ directory

[DBpedia](http://data.dws.informatik.uni-mannheim.de/kgvec2go/iswc/dbpedia_500_4_sg_200/)

[Wikidata](https://zenodo.org/record/827339#.YeMlCP7MJD8)

[UMLS](https://tib.eu/cloud/s/smHP3TTR9Z6B9XH)

## The PINYON SCD Approach

Now that we have all the necessary data, we can run the PINYON approach against the three KGs (UMLS, Wikidata, and DBpedia).
For example, to run the approach against UMLS, please use the following:

```
python3 run_umls.py
```


