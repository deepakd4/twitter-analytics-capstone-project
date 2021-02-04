from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from kafka import KafkaProducer
import json
import logging
import configparser
from datetime import datetime
from datetime import timezone

config = configparser.RawConfigParser()
config.read('config.cfg')

ACCESS_TOKEN = config.get('Twitter', 'access_token')
ACCESS_TOKEN_SECRET = config.get('Twitter', 'access_token_secret')
CONSUMER_KEY = config.get('Twitter', 'consumer_key')
CONSUMER_SECRET = config.get('Twitter', 'consumer_secret')
# TWITTER_STREAMING_MODE = config.get('Twitter', 'streaming_mode')
KAFKA_ENDPOINT = '{0}:{1}'.format(config.get('Kafka', 'kafka_endpoint'), config.get('Kafka', 'kafka_endpoint_port'))
KAFKA_TOPIC = config.get('Kafka', 'topic')


class TwitterProducer(StreamListener):

    def on_data(self, data):
        producer = self.create_kafka_producer()
        producer.send(KAFKA_TOPIC, key=None, value=data).add_callback(self.on_send_success).add_errback(
            self.on_send_error)
        print(data)
        return True

    def on_error(self, status):
        print(status)

    def create_kafka_producer(self):
        producer = KafkaProducer(bootstrap_servers=KAFKA_ENDPOINT,
                                 value_serializer=lambda m: json.dumps(m).encode('ascii'))
        return producer

    def on_send_success(self, record_metadata):
        print(record_metadata.topic)
        print(record_metadata.partition)
        print(record_metadata.offset)

    def on_send_error(self, excp):
        logging.error('error in sending message to kafka topic', exc_info=excp)
        # handle exception


if __name__ == '__main__':
    twitter_producer = TwitterProducer()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
    stream = Stream(auth, twitter_producer)
    stream.filter(track=["#AI", "#DataScince", "MachineLearning", "DeepLearning"], languages=["en"])