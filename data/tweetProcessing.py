import json
import re
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords
import csv
import textblob

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

states = ["Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado", "Connecticut", "Delaware", "Florida",
          "Georgia", "Hawaii", "Idaho",
          "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", "Massachusetts",
          "Michigan", "Minnesota", "Mississippi",
          "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York",
          "North Carolina", "North Dakota",
          "Ohio", "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", "Tennessee",
          "Texas", "Utah",
          "Vermont", "Virginia", "Washington", "West Virginia", "Wisconsin", "Wyoming"]


# tweet pre processor adapted for project use from https://gist.github.com/AnasAlmasri/af0b92428b00708b4cc710370ff3c82e#file-sentimentanalysis-py
def processTweet(tweet):
    stop_words = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])
    tweet = tweet.lower()  # convert text to lower-case
    tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
    tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
    tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove any usernames in the tweet
    tweet = word_tokenize(tweet)  # remove repeated or unnecessary characters
    return [word for word in tweet if word not in stop_words]


def processTrainingData(file):
    with open(file) as csvFile:
        trainingData = []
        reader = csv.reader(csvFile)
        for line in reader:
            processed_text = processTweet(line[1])
            label = line[2]
            trainingData.append((processed_text, label))

    return trainingData


def processTweets(file, training=False):
    with open(file) as jsonFile:
        # if you haven't run the script yet, you need to uncomment these and run them
        # nltk.download('stopwords')
        # nltk.download('punkt')

        processedData = []
        data = []

        for line in jsonFile:
            try:
                data.append(json.loads(line))
            except json.decoder.JSONDecodeError:
                continue

        # grab date, text, and state from tweet data
        for i in data:
            # get the text
            try:
                text = i['extended_tweet']['full_text']
            except KeyError:
                text = i['text']

            processed_text = processTweet(text)

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

            if state in states:  # make sure its a legit state
                processedData.append((processed_text, state, day, text))

    jsonFile.close()
    return processedData


# adapted for project use from https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed
class ClassificationVocab:
    def __init__(self):
        self.wordFeatures = []

    def buildWordVocab(self, tweets):
        words = []
        for tweet in tweets:
            for word in tweet[0]:
                words.append(word)
        wordList = nltk.FreqDist(words)
        self.wordFeatures = wordList.keys()

    def getWordFeatures(self, tweet):
        tweet_words = set(tweet)
        return dict([(word, word in tweet_words) for word in self.wordFeatures])

def main():
    # get the training data and the testing data
    trainingData = processTrainingData('trainingData.csv')  # file with training data (pre classified tweets)
    testData = processTweets('tweets-sarah.json', False)  # file with tweets to classify
    testData.extend(processTweets('tweets-allison.json'))
    testData.extend(processTweets('tweets-hunter.json'))

    # build our vocab for our model
    vocab = ClassificationVocab()
    vocab.buildWordVocab(trainingData)
    trainingFeatures = nltk.classify.apply_features(vocab.getWordFeatures, trainingData)

    # train the model!
    classifier = nltk.NaiveBayesClassifier.train(trainingFeatures)

    # classify the testing data
    classifiedLabels = []
    actualLabels = []
    correct = 0
    for tweet in testData:
        text = tweet[0]
        processed_tweet = ""
        for word in text:
            processed_tweet += word + " "
        classifiedLabels.append(classifier.classify(vocab.getWordFeatures(text)))
        blob = textblob.TextBlob(processed_tweet)
        sentiment = blob.sentiment.polarity
        if sentiment <= 0:
            actualLabels.append('negative')
        else:
            actualLabels.append('positive')

    #to see the tweets & how they're classified, uncomment this!
    for i in range(0, len(classifiedLabels)):
        if classifiedLabels[i] == actualLabels[i]:
            #print([testData[i][3], testData[i][0], classifiedLabels[i], actualLabels[i]])
            correct += 1

    # calculate accuracy of our vocab in comparison with text blob
    print("Accuracy: ", correct / len(classifiedLabels))

    # get rid of the tweet text & match the label to the state/day for that tweet
    classifiedTestData = []
    for i in range(0, len(testData)):
        label = classifiedLabels[i]
        classifiedTestData.append([testData[i][0], testData[i][1], testData[i][2], label])

    #print(classifiedTestData)
    print("Positive tweets: ", classifiedLabels.count('positive'), "Negative tweets: ",
          classifiedLabels.count('negative'))

    csvFile = open('test.csv', 'a')
    csvWriter = csv.writer(csvFile)

    for line in classifiedTestData:
        csvWriter.writerow([line[1], line[2], line[3]])

    csvFile.close()


main()
