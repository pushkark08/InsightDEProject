# Insight DE Project
Insight Data Engineering project

# Idea
Take incoming tweets, extract important keywords from them, link them with their wikipedia page and output the tweet with this additional information.

# Purpose and Use case
Imagine you are reading a tweet about a person/location/concept and you are interested in knowing more about it. You will have to go on Google and search more about it manually. It will be very useful if you can just click on that entity and go to its wikipedia page to know more about it.
It is very easy to increase the scope of this project and add multiple sources of information for the user. Also the input can be changed to news articles/restaurant reviews etc.

# Technologies
S3, Kafka, Spark Streaming, Elastic Search, PostgreSQL

# Challenges
1. Outputting streaming tweets as fast as possible
2. Extract keywords and link it to Wikipedia

# Architecture
![Screenshot](Pipeline.png)
