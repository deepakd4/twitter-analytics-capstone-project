from elasticsearch import Elasticsearch
from kafka import KafkaConsumer
import json
import configparser


config = configparser.RawConfigParser()
config.read('config.cfg')

es = Elasticsearch(hosts=['localhost'], port=9200)
KAFKA_TOPIC = config.get('Kafka', 'topic')

def main():

    consumer = KafkaConsumer(KAFKA_TOPIC, value_deserializer=lambda m: json.loads(m.decode('ascii')),
                             auto_offset_reset='earliest')

    for msg in consumer:
        print(type(msg))
        print(msg)

        dict_data = json.loads(msg.value)
        print(dict_data)

        es.index(
                    index="tweet_index",
                    doc_type="test_doc",
                    body={
                    "author": dict_data["user"]["screen_name"],
                    "date": dict_data["created_at"],
                    "message": dict_data["text"]
                    }
                )
        print(dict_data)
        print('\n')


if __name__ == "__main__":
    main()