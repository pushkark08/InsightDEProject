from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import json

access_token = "<your-access-token>"
access_token_secret = "<your-access-token-secret>"
consumer_key = "<your-consumer-key>"
consumer_secret = "<your-consumer-secret>"

topic = "allTweets"

class TweetListener(StreamListener):

	def on_data(self, data):
        json_data = json.loads(data)
        rt = json_data.get('retweeted_status')
        if rt is not None:
            if rt.get('extended_tweet') is not None:
                producer.send(topic, key=str(json_data['created_at']), value=rt['extended_tweet']['full_text'].encode('ascii', 'replace'))
            else:
                producer.send(topic, key=str(json_data['created_at']), value=rt['text'].encode('ascii', 'replace'))
        else:
            if json_data.get('extended_tweet') is not None:
                producer.send(topic, key=str(json_data['created_at']), value=json_data['extended_tweet']['full_text'].encode('ascii', 'replace'))
            else:
                producer.send(topic, key=str(json_data['created_at']), value=json_data['text'].encode('ascii', 'replace'))
        return True

    def on_error(self,statusCode):
        print "Error Code: %s"%statusCode
        return True

ipfile = open('<ip file>', 'r')
ips = ipfile.read()
ipfile.close()
ips = ips.split(', ')

producer = KafkaProducer(bootstrap_servers=ips)

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
stream = Stream(auth, TweetListener())

words_to_track = "a the to and is in it you of for on my that at with me do have just this be so are not was but out up what now new from your like good no get all about we if time as day will one how can some an am by going they go or has know today there love more work too got he back think did when see really had great off would need here thanks been still people who night want why home should well much then right make last over way does getting watching its only her post his morning very she them could first than better after tonight our again down news man us tomorrow best into any hope week nice show yes where take check come fun say next watch never bad free life".split()

# ids_to_follow = ['21447363','27260086','79293791','17919972','14230524','26565946','25365536','34507480','783214','807095','759251','180505807',
# '2557521','5402612','5988062','742143','1367531','28785486','326359913','1115874631','813286','25073877','18839785','11348282',
# '471741741','822215679726100480','1339835893','20609518','822215673812119553','500704345']
stream.filter(languages=["en"], track=words_to_track)
