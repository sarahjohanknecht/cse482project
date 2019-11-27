import csv
import time
import twitter

def buidTrainingSet(corpusFile, tweetDataFile):
    corpus = []
    # initialize api instance
    twitter_api = twitter.Api(consumer_key='JYo9isJyYHekNIWeO1N6nPwmn',
                              consumer_secret='YihdlaZ4itMRpM2otcR5bGpkR7LgJrJdY7Vz5QQcAzLKTmSzwa',
                              access_token_key='2807633071-UQ122PnRmEJs2A5A9EokHJZ0uzy9zQ7847ijP2n',
                              access_token_secret='cQGhzBpWdlUDWeFid9wYDyPATdhDsOWR7rluByYqS3nGM')

    # test authentication
    print(twitter_api.VerifyCredentials())
    with open(corpusFile, 'r') as csvfile:
        lineReader = csv.reader(csvfile, delimiter=',', quotechar="\"")
        for row in lineReader:
            corpus.append({"tweet_id": row[2], "label": row[1], "topic": row[0]})

    rate_limit = 180
    sleep_time = 900 / 180

    trainingDataSet = []

    writeFile = open(tweetDataFile, 'w')
    linewriter = csv.writer(writeFile, delimiter=',', quotechar="\"")

    for tweet in corpus:
        if tweet["label"] == "positive" or tweet["label"] == "negative":
            try:
                status = twitter_api.GetStatus(tweet["tweet_id"])
                print("Tweet fetched" + status.text)
                tweet["text"] = status.text
                trainingDataSet.append(tweet)
                time.sleep(sleep_time)
            except:
                continue

            try:
                linewriter.writerow([tweet["tweet_id"], tweet["text"], tweet["label"], tweet["topic"]])
                print("success")
            except Exception as e:
                print(e)

    writeFile.close()
    return trainingDataSet

def main():
    buidTrainingSet('corpus.csv', 'trainingData.csv')

main()