import csv

states = ["Alabama","Alaska","Arizona","Arkansas","California","Colorado","Connecticut","Delaware","Florida","Georgia","Hawaii","Idaho",
"Illinois","Indiana","Iowa","Kansas","Kentucky","Louisiana","Maine","Maryland","Massachusetts","Michigan","Minnesota","Mississippi",
"Missouri","Montana","Nebraska","Nevada","New Hampshire","New Jersey","New Mexico","New York","North Carolina","North Dakota",
"Ohio","Oklahoma","Oregon","Pennsylvania","Rhode Island","South Carolina","South Dakota","Tennessee","Texas","Utah",
"Vermont","Virginia","Washington","West Virginia","Wisconsin","Wyoming"]


fp = open('testing.csv')
csvFile = open('aggregatedData', 'a')
csvWriter = csv.writer(csvFile)

csvWriter.writerow(['State', 'Sent', 'Date'])
reader = csv.reader(fp)
line = next(reader)
current_date = line[1]
fp.seek(0)

day_dict = {}
for line in reader:
    date = line[1]
    state = line[0]
    sentiment = line[2]
    if state not in states:
        continue
    if state not in day_dict:
        day_dict[state] = {'positive': 0, 'negative': 0}
    day_dict[state][sentiment] += 1

    if date != current_date:

        print(day_dict)
        for state in day_dict:
            positive = day_dict[state]['positive']
            total = day_dict[state]['positive'] + day_dict[state]['negative']
            sentiment_ratio = int(positive/total*100)
            print(state, current_date, sentiment_ratio)
            write_date = int(current_date)
            csvWriter.writerow([state, sentiment_ratio, write_date])

        current_date = date

csvFile.close()
