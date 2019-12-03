import csv

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
"Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
"Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


fp = open('sentiment-testing.csv')
csvFile = open('aggregatedData-final.csv', 'a')
csvWriter = csv.writer(csvFile)

csvWriter.writerow(['State', 'Sent', 'Date'])
reader = csv.reader(fp)
line = next(reader)
current_date = line[1]
fp.seek(0)

day_dict = {}         # create an empty dictionary for each day
for line in reader:   # iterate through mass data file
    date = line[1]
    state = line[0]
    sentiment = line[2]
    if state not in states:   # get rid of invalid state data
        continue
    # if the state is not in the dictionary yet for that day, add it
    if state not in day_dict:
        day_dict[state] = {'positive': 0, 'negative': 0}
    # once the state is in the day dict, add to either pos or neg based on that tweets sentiment
    day_dict[state][sentiment] += 1

    # if the date changes, we need to total up the sentiment
    if date != current_date:
        # total up each states sentiment for that day
        for state in day_dict:
            positive = day_dict[state]['positive']
            total = day_dict[state]['positive'] + day_dict[state]['negative']
            # ratio is the positive sentiment over the total (number between 0-100)
            sentiment_ratio = int(positive/total*100)
            print(state, current_date, sentiment_ratio)
            write_date = int(current_date)
            csvWriter.writerow([state, sentiment_ratio, write_date])

        current_date = date

csvFile.close()
