import csv
import time
import twitter


# script adapted from https://towardsdatascience.com/creating-the-twitter-sentiment-analysis-program-in-python-with-naive-bayes-classification-672e5589a7ed

def getTrainingData(corpusFile, tweetDataFile):
    trainingData = []

    #read in the training data csv file (downloaded from https://github.com/karanluthra/twitter-sentiment-training)
    readFile = open(corpusFile, 'r')
    lineReader = csv.reader(readFile, delimiter=',', quotechar="\"")
    for row in lineReader:
        trainingData.append({"tweet_id": row[2], "label": row[1], "topic": row[0]})


    # initialize api instance - set these to your Twitter API keys
    twitterAPI = twitter.Api(consumer_key='',
                              consumer_secret='',
                              access_token_key='',
                              access_token_secret='')

    sleepTime = 6
    downloadedTrainingData = []
    writeFile = open(tweetDataFile, 'w')
    lineWriter = csv.writer(writeFile, delimiter=',', quotechar="\"")

    for tweet in trainingData:
        if tweet["label"] == "positive" or tweet["label"] == "negative":
            try:
                status = twitterAPI.GetStatus(tweet["tweet_id"])
                print("Tweet fetched" + status.text)
                tweet["text"] = status.text
                downloadedTrainingData.append(tweet)
                time.sleep(sleepTime)

            except Exception as e:
                print(e)
                continue

            try:
                lineWriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"]])
                print("success")

            except Exception as e:
                print(e)

    writeFile.close()
    readFile.close()
    return downloadedTrainingData


def main():
    getTrainingData('corpus.csv', 'trainingData.csv') #send the file to read training data from, and the file to write training data to

main()
