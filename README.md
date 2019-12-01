# cse482project
Twitter Sentiment Analysis Project for CSE 482 (Big Data Analysis)

Website: http://bigdata-tweetanalysis.herokuapp.com/tweets/

Project description: http://cse.msu.edu/~liuhaoc1/cse482/class_project.html


## How it works:
1. Apply for Twitter API Credentials
2. Run TweetQuery.ipynb for the desired period of time to collect tweets pertaining to the subject. We ran our script for an hour everyday over a period of a month, collecting data about President Donald Trump.
3. Run getTrainingData.py using the corpus.csv file to collect pre-classified tweets with positive or negative sentiment. This is the training data used to train the Naive Bayes Classifier. This script could take a few hours to run!
4. Run TweetProcessing.py on your data file that consists of the tweets collecting from step #2. This takes in the raw data of the tweet and processes it to get the day, location, and raw text of the tweet (that is then preprocessed). It then uses the training data to train a Naive Bayes Classifier, then uses that classifier to predict the sentiment for the collected tweets.
5. Run aggregateData.py on the processed tweet file. This takes in the data for every single tweet (its location, day, and predicted sentiment), and aggregates the data by state per day, calculating the tweet sentiment for that day (positive tweets/total tweets). 
6. Run generatemaps.py on the aggregated data file. This takes in the aggregated data and turns it into maps to visualize the tweet sentiment.

Website hosted using Django and Heroku. Tweets processed and classified with help of the NLTK library. Sentiment maps generated using geopandas library.
