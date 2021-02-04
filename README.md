# twitter-analytics-capstone-project

This is my capstone project for MS Business Analytics program at CSU East Bay.

### Overview
This a data engineering project that uses some tools in big data engineering space to build a data pipeline. 

This data pipeline collects data from twitter api, publish it to a kafka topic. Two consumers, an Elasticsearch search service and a PostgresSQL service consume from this Kafka Topic.
The data is indexed in Elasticsearch and visualized in Kibana.

[Twitter Analytics Pipeline](./Real%20Time%20Tweets%20Analytics.jpg)



### Twitter API
Real time tweets with keywords of interests such as #AI, #DataScience, #MachineLearing, #DeepLearning are fetched. 
The data source is Twitter Filter Stream API.
<https://developer.twitter.com/en/docs/twitter-api/tweets/filtered-stream/api-reference/get-tweets-search-stream>
A python library called Tweepy <https://www.tweepy.org/> is used to interact with the Twitter API. Tweepy provides an easy to use interface over the Twitter API.


### Apache Kafka
A kafka topic called twitter-tweets is created. Currently there is just 1 partition for this topic. All the configuration for this topic are default. 


### Elasticsearch
An elasticsearch index called twitter-tweets stores the documents with information abouot tweet author, tweet created timestamp and tweet text.


### Kibana
Elasticsearch and Kibana are tightly coupled. We can easily visualize the data stored in elasticsearch. 