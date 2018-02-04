from pyspark import SparkContext, SparkConf
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
from elasticsearch import Elasticsearch
from nltk import pos_tag,word_tokenize, ne_chunk
from nltk.tree import Tree
import re
import requests
import string
import pgdb
import copy, requests
import json, time
import sys

reload(sys)
sys.setdefaultencoding('utf8')

sp_config = SparkConf().setAppName("SparkStreamingKafkaES")
sc = SparkContext(conf = sp_config)
sc.setLogLevel("WARN")
log4jlogger = sc._jvm.org.apache.log4j
logger = log4jlogger.LogManager.getLogger(__name__)
logger.warn("okay done")

elastic_nodes = [<your-es-cluster-nodes>]
elastic = Elasticsearch(elastic_nodes, http_auth=('elastic', 'changeme'))

batch_duration = 3
ssc = StreamingContext(sc, batch_duration)
topic = ["allTweets"]
kafka_params = {"metadata.broker.list": "<your-brokers>"}
kafka_stream = KafkaUtils.createDirectStream(ssc, topic, kafka_params)


url_stop_words="http://www.mit.edu/~ecprice/wordlist.10000"
response= requests.get(url_stop_words)

def get_stopwords():
	common_words=response.content.split("\n")
	common_tweet_stopwords=["RT","co"]
	stop_words=common_tweet_stopwords+common_words
	return stop_words

	
def preprocess(tweet):
	tweet = re.sub(r'(https|http)?:\/\/(\w|\.|\/|\?|\=|\&|\%)*\b', "", tweet)
	return tweet


# from nltk.tag import StanfordNERTagger
# from nltk.tokenize import word_tokenize
# st = StanfordNERTagger('/usr/share/stanford-ner/classifiers/english.all.3class.distsim.crf.ser.gz',
# 					   '/usr/share/stanford-ner/stanford-ner.jar', encoding='utf-8')
# text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'
# tokenized_text = word_tokenize(text)
# classified_text = st.tag(tokenized_text)
# print(classified_text)

	
def process(tweet):
	tokens = word_tokenize(tweet)
	entity_tree = ne_chunk(pos_tag(tokens), binary=False)
	
	named_entity = []
	current_chunk = []
	for i in entity_tree:
		if type(i) == Tree:
			current_chunk.append(" ".join([token for token, pos in i.leaves()]))
		elif current_chunk:
			entity = " ".join(current_chunk)
			if entity not in named_entity:
				named_entity.append(entity)
				current_chunk = []
		else:
			continue
	if current_chunk:
		entity = " ".join(current_chunk)
		if entity not in named_entity:
			named_entity.append(entity)
			current_chunk = []

	token_positions = []
	for i in range(len(tokens)):
		if tokens[i] in named_entity:
			token_positions.append(i)
	return (tokens, token_positions)


def store(rdd):
	row_rdd = rdd.collect()

	stop_words = get_stopwords()
	old_new_tweets = []
	
	for row in row_rdd:
		tokens = row[0]
		original_tokens = copy.deepcopy(tokens)
		original_tweet = " ".join(t for t in original_tokens)
		positions = row[1]
		title_output = []
		
		for pos in positions:
			query_word = tokens[pos]
			if query_word.lower() not in stop_words:
				
				# query = {"_source" : ["title"], "size":1, "query": { "multi_match": {  "query": query_word,  "type":"best_fields", 
				# "fields": [ "title", "text" ],  "tie_breaker": 0.3, "minimum_should_match": "30%"  } } }
				
				query = {"_source": ["title"], "size":1, "query":{"match_phrase" : {"text" : {"query" : query_word}}}}
				search_output = elastic.search(index="en_wikipedia", body=query)

				if search_output is not None:
					if search_output['hits'] is not None:
						if len(search_output['hits']['hits']) > 0:
							new_word = search_output['hits']['hits'][0]['_source']['title']
							new_word = new_word.replace(" ", "_")
							tokens[pos] = " <a href=\'http://en.wikipedia.com/wiki/" + new_word + "\''>"  + tokens[pos] + "</a>" 

		new_tweet = " ".join(t.encode('ascii', 'replace') for t in tokens)
		
		if original_tweet != new_tweet:
			old_new_tweets.append((original_tweet, new_tweet))
		
	put_in_db(connection, old_new_tweets)


hostname = '<ip>'
username = '<db-username>'
password = '<db-pwd>'
database = '<db-name>'
connection = pgdb.connect(host=hostname, user=username, password=password, database=database)

def put_in_db(conn, tweet_tuple):	
	cur = conn.cursor()

	insert_query = "INSERT INTO tweets (original_tweet, enriched_tweet) VALUES (%s, %s)"
	
	cur.executemany(insert_query, tweet_tuple)
	conn.commit()
	cur.close()

	
tweet_stream = kafka_stream.map(lambda y : y[1].encode('utf-8')).map(lambda p : preprocess(p))
processed_tweets = tweet_stream.map(lambda t : process(t))
filtered_tweets = processed_tweets.filter(lambda c : len(c[1]) > 0)
filtered_tweets.foreachRDD(store)
	
ssc.start()
ssc.awaitTermination()
conn.close()