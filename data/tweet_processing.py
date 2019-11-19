import json

state_dict = {"AL":"Alabama","AK":"Alaska","AZ":"Arizona","AR":"Arkansas",
              "CA":"California","CO":"Colorado","CT":"Connecticut",
              "DE":"Delaware","DC":"District of Columbia","FL":"Florida",
              "GA":"Georgia","HI":"Hawaii","ID":"Idaho","IL":"Illinois",
              "IN":"Indiana","IA":"Iowa","KS":"Kansas","KY":"Kentucky",
              "LA":"Louisiana","ME":"Maine","MT":"Montana","NE":"Nebraska",
              "NV":"Nevada","NH":"New Hampshire","NJ":"New Jersey",
              "NM":"New Mexico","NY":"New York","NC":"North Carolina",
              "ND":"North Dakota","OH":"Ohio","OK":"Oklahoma","OR":"Oregon",
              "MD":"Maryland","MA":"Massachusetts","MI":"Michigan",
              "MN":"Minnesota","MS":"Mississippi","MO":"Missouri",
              "PA":"Pennsylvania","RI":"Rhode Island","SC":"South Carolina",
              "SD":"South Dakota","TN":"Tennessee","TX":"Texas","UT":"Utah",
              "VT":"Vermont","VA":"Virginia","WA":"Washington",
              "WV":"West Virginia","WI":"Wisconsin","WY":"Wyoming"}


with open('tweets-hunter.json') as json_file:
    count = 1
    data = []
    for line in json_file:
        try:
            data.append(json.loads(line))
        except json.decoder.JSONDecodeError:
            continue

    for i in data:
        #grab date, text, and state from tweet data
        text = i['text'] #tweet text

        date = i['created_at'].split(" ")
        day = date[2] #day

        place = i['place']['full_name']
        places = place.split(", ")
        state = "" #state
        if len(places) > 1:
            if places[1] == "USA":
                state = places[0]
            elif len(places[1]) == 2:
                state = state_dict[place[place.index(',')+2:]]
            else:
                #bad data, so skip
                state = ""
                continue

        #preprocess text

        #write to csv file
