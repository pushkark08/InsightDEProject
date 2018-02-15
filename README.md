# WIKIFY
This is my Insight Data Engineering project which I completed in 3 weeks in Jan 2018.

# Idea
Suppose you come across a completely new term while reading an article or scrolling through your twitter feed and you are interested in knowing more about it. So what you would generally do is copy the text, search it on Google and read more from the links it provides. Instead of doing all this, what if you could just click on the word that interests you and it would take you to either its wikipedia page or any other source of information which would enhance your experience. This is the motivation behind this project.

# Use case
There are many use cases for this idea.  Depending on the use-case, we can add multiple sources of information for the user instead of just wikipedia. Also, the input text can be restaurant reviews in which we find the names of dishes and link them to their nutritional information/recipe page.

# Implementation
Tweets are ingested in real-time using Kafka which are then processed using Spark streaming to obtain key terms from the tweet text using NLTK libraries. I also tried the Stanford Core NLP tool but found it to give similar performance as NLTK. In Elasticsearch I have indexed approx 55 million wikipedia pages which are queried for the key terms in spark streaming component. Finally the enriched tweet is stored in postgresql database and retrieved in Flask to display on the webpage.

Different types of elasticsearch queries take different amounts of time. If I search for a query term in the complete text and title of the wikipedia pages, I can complete approx. 11700 searches/min. Whereas if I only search in the titles of wikipedia pages, I can do 19000 searches/min. So there is a tradeoff between search accuracy and processing time which should considered for a specific use case.

# Future Work
There is a lot of scope for improvement in the NLP module which extracts the key entities from the text. A custom NLP module can be built and substituted for the NLTK libraries.

# Slides and Demo
http://slides.wikify.club

http://wikify.club

# Architecture
![Screenshot](Pipeline.png)
