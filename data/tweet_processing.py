import json

import re
import nltk
from nltk.tokenize import word_tokenize
from string import punctuation
from nltk.corpus import stopwords

import csv

state_dict = {"AL": "Alabama", "AK": "Alaska", "AZ": "Arizona", "AR": "Arkansas",
              "CA": "California", "CO": "Colorado", "CT": "Connecticut",
              "DE": "Delaware", "DC": "District of Columbia", "FL": "Florida",
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

#tweet pre processor from https://gist.github.com/AnasAlmasri/af0b92428b00708b4cc710370ff3c82e#file-sentimentanalysis-py
#adapted for project use
class PreProcessTweets:
    def __init__(self):
        self._stopwords = set(stopwords.words('english') + list(punctuation) + ['AT_USER', 'URL'])

    def processTweet(self, tweet):
        tweet = tweet.lower()  # convert text to lower-case
        tweet = re.sub('((www\.[^\s]+)|(https?://[^\s]+))', 'URL', tweet)  # remove URLs
        tweet = re.sub('@[^\s]+', 'AT_USER', tweet)  # remove usernames
        tweet = re.sub(r'#([^\s]+)', r'\1', tweet)  # remove the # in #hashtag
        tweet = word_tokenize(tweet)  # remove repeated characters (helloooooooo into hello)
        return [word for word in tweet if word not in self._stopwords]

with open('tweets-hunter.json') as json_file:
    #if you haven't run the script yet, you need to uncomment these and run them
    #nltk.download('stopwords')
    #nltk.download('punkt')
    processor = PreProcessTweets()

    count = 1
    data = []
    tweets = []
    for line in json_file:
        try:
            data.append(json.loads(line))
        except json.decoder.JSONDecodeError:
            continue

    for i in data:
        # grab date, text, and state from tweet data
        try:
            text = i['extended_tweet']['full_text']
        except KeyError:
            text = i['text']
        processed_text = processor.processTweet(text)

        date = i['created_at'].split(" ")
        day = date[2]  # day

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
                state = ""
                continue
        print(processed_text, day, state)


    #write to csv
    csvFile = open('processed_data.csv', 'a')
    csvWriter = csv.writer(csvFile)
    #csvWriter.writerow([text, state, day]) #uncomment this to write to the file

csvFile.close()
json_file.close()