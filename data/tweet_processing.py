import json
import re
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
from textblob import TextBlob
import csv

state_dict = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
              "CA": "California", "CO": "Colorado", "CT": "Connecticut",
              "DE": "Delaware", "DC": "Virginia", "FL": "Florida",
              "GA": "Georgia", "HI": "Hawaii", "ID": "Idaho", "IL": "Illinois",
              "IN": "Indiana", "IA": "Iowa", "KS": "Kansas", "KY": "Kentucky",
              "LA": "Louisiana", "ME": "Maine", "MT": "Montana", "NE": "Nebraska",
              "NV": "Nevada", "NH": "New Hampshire", "NJ": "New Jersey",
              "NM": "New Mexico", "NY": "New York", "NC": "North Carolina",
              "ND": "North Dakota", "OH": "Ohio", "OK": "Oklahoma", "OR": "Oregon",
              "MD": "Maryland", "MA": "Massachusetts", "MI": "Michigan",
              "MN": "Minnesota", "MS": "Mississippi", "MO": "Missouri",
              "PA": "Pennsylvania", "RI": "Rhode Island", "SC": "South Carolina",
              "SD": "South Dakota", "TN": "Tennessee", "TX": "Texas", "UT": "Utah",
              "VT": "Vermont", "VA": "Virginia", "WA": "Washington",
              "WV": "West Virginia", "WI": "Wisconsin", "WY": "Wyoming"}

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
"Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
"Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


# tweet pre processor from https://gist.github.com/AnasAlmasri/af0b92428b00708b4cc710370ff3c82e#file-sentimentanalysis-py
# adapted for project use
class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

    def processTweet(self, tweet):
        tweet = tweet.lower()  # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
        tweet = word_tokenize(tweet)  # remove repeated characters
        return [word for word in tweet if word not in self._stopwords]


def processTweets(file, training=False):
    with open(file) as jsonFile:
        # if you haven't run the script yet, you need to uncomment these and run them
        # nltk.download('stopwords')
        # nltk.download('punkt')

        processor = PreProcessTweets()
        processedData = []
        data = []

        for line in jsonFile:
            try:
                data.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                continue

        negCount = 0
        posCount = 0
        neuCount = 0

        # grab date, text, and state from tweet data
        for i in data:
            # get the text
            try:
                text = i['extended_tweet']['full_text']
            except KeyError:
                text = i['text']

            # calculate the tweet sentiment if we are processing training data
            if training:
                sentiment = TextBlob(text).sentiment.polarity

                if sentiment >= 0.25:
                    pos_neg = "positive"
                    posCount += 1
                elif sentiment <= -0.25:
                    pos_neg = "negative"
                    negCount += 1
                else:
                    pos_neg = "neutral"
                    neuCount += 1

            processed_text = processor.processTweet(text)

            # get the day
            date = i['created_at'].split(" ")
            day = date[2]  # day

            # get the state
            place = i['place']['full_name']
            places = place.split(", ")
            state = ""  # state
            if len(places) > 1:
                if places[1] == "USA":
                    state = places[0]
                elif len(places[1]) == 2:
                    state = state_dict[place[place.index(',') + 2:]]
                else:
                    # bad data, so skip
                    continue

            # collect data to return
            if training:
                # only use strongly positive/strongly negative data to train!
                if pos_neg == "positive" or pos_neg == "negative":
                    processedData.append((processed_text, pos_neg))

            else:
                if state in states: # make sure its a legit state
                    processedData.append((processed_text, state, day))

    print(posCount, negCount, neuCount)
    jsonFile.close()
    return processedData


class Model:
    def __init__(self):
        self.wordFeatures = []

    def buildVocabulary(self, data):
        words = []

        for tweet in data:
            for word in tweet[0]:
                words.append(word)

        wordList = nltk.FreqDist(words)
        wordFeatures = wordList.keys()
        self.wordFeatures = wordFeatures

    def features(self, tweet):
        tweet_words = set(tweet)
        features = {}
        for word in self.wordFeatures:
            features['contains(%s)' % word] = (word in tweet_words)
        return features


def main():
    # get the training data and the testing data
    trainingData = processTweets('tweets-sarah.json', True)
    testData = processTweets('tweets-hunter.json', False)

    # build our vocab for our model
    model = Model()
    model.buildVocabulary(trainingData)
    trainingFeatures = nltk.classify.apply_features(model.features, trainingData)

    # train the model!
    classifier = nltk.NaiveBayesClassifier.train(trainingFeatures)

    # classify the testing data
    classifiedLabels = [classifier.classify(model.features(tweet[0])) for tweet in testData]

    # get rid of the tweet text & match the label to the state/day for that tweet
    classifiedTestData = []
    for i in range(0, len(testData)):
        label = classifiedLabels[i]
        classifiedTestData.append([testData[i][0], testData[i][1], testData[i][2], label])

    print("Positive tweets: ", classifiedLabels.count('positive'), "Negative tweets: ",
          classifiedLabels.count('negative'))

    csvFile = open('testing.csv', 'a')
    csvWriter = csv.writer(csvFile)

    for line in classifiedTestData:
        csvWriter.writerow([line[1], line[2], line[3]])

    csvFile.close()


main()
