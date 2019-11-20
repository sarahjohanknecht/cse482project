import nltk
import csv




def buildVocabulary(reader):
    all_words = []
    #make a list of list of all tweets
    all_tweets = []
    for line in reader:
        text = line[0]
        words = text.split()
        all_tweets.append(words)
        #add to the list of all words
        all_words.extend(words)
        print(all_words)

        wordlist = nltk.FreqDist(all_words)
        word_features = wordlist.keys()

    return word_features,all_tweets


def extract_features(tweet):
    tweet_words = set(tweet)
    features = {}
    for word in vocab:
        features['contains(%s)' % word] = (word in tweet_words)
    return features

fp = open('processed_data.csv')
reader = csv.reader(fp)

vocab, all_tweets = buildVocabulary(reader)

#print(all_tweets)

trainingFeatures = nltk.classify.apply_features(extract_features, all_tweets)

print(trainingFeatures)



