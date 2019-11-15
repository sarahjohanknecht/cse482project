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


with open('tweets.json') as json_file:
    data = json.load(json_file)
    #for i in data:
    print("\ntext:", data['text'])
    #print("\ncreated_at:", data['created_at'])
    place = data['place']['full_name']
    state = state_dict[place[place.index(',')+2:]]
    print(state)
