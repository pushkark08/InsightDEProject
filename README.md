# Insight DE Project
Wikify - Insight Data Engineering project

# Idea
Suppose you come across a completely new term while reading an article or scrolling through your twitter feed and you are interested in knowing more about it. You would generally copy the text, search it on Google and read more about it. Instead of doing all this, what if you could just click on the word that interests you and it would take you to either its wikipedia page or any other source of information. This is the motivation behind this project.

# Use case
The scope of this project is very huge. We can add multiple sources of information for the user depending on the use-case. Also, the input can be changed to news articles/restaurant reviews etc.

# Implementation
Tweets are ingested in real-time using Kafka which are then processed using Spark streaming to obtain key terms from the tweet text using NLTK libraries. I have indexed 55 million wikipedia pages in elasticsearch which are queried from spark streaming. The enriched text is stored in postgresql database and retrieved in Flask to display on the webpage.

Different types of elasticsearch queries take different amounts of time. If we search for a query term in the complete text and title of the wikipedia pages, we can complete approx. 11700 searches/min. Whereas if we only search in the titles of wikipedia pages, we can do 19000 searches/min. So there is a tradeoff between search accuracy and processing time. 

# Future Work
There is a lot of scope for improvement in the NLP module which extracts the key entities from the text. A custom NLP module can be built and substituted for the NLTK libraries. 

# Architecture
![Screenshot](Pipeline.png)
