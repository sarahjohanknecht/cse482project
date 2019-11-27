import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.colors as colors

NUM_DAYS = 8  # set this to the number of days we are collecting data for PLUS ONE
DATES = [1,2,3,4,5,6,7,8,9,11,12,13,14,15,16,18,30,31]  # this needs to be changed we we have data from every day
#DATES = [1]
DATAFILE = '/Users/sarahjohanknecht/F19/cse482/cse482project/tweetanalysis/data/aggregatedData-final.csv'  # file to read data from

# read in map shp file
shpPath = "ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp"
mapDF = gpd.read_file(shpPath)

DFByDay = []  # list to hold each dataframe for each day's data

# read states sentiment data
df = pd.read_csv(DATAFILE)
print(df.head())

# split the data frame into data frames by day
for date in DATES:
    dfDay = df[df['Date'] == date]
    dfDay.columns = ["State", "Sent", "Date"]
    DFByDay.append(dfDay)

# generate map for each day
for day in DFByDay:
    print(day)
    # join map data with sentiment data
    merged = mapDF.set_index('name').join(day.set_index("State"))

    # visualize the data
    variable = 'Sent'
    fig, ax = plt.subplots(1, figsize=(10, 6))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="2%", pad=0.1)
    vmin, vmax, vcenter = 0, 100, 50
    divnorm = colors.DivergingNorm(vmin=vmin, vmax=vmax, vcenter=50)
    cbar = plt.cm.ScalarMappable(norm=divnorm, cmap='Purples')
    usMap = merged.plot(column=variable, cmap='Purples', linewidth=1.0, ax=ax, edgecolor='0', legend=True, cax=cax,
                        legend_kwds={'label': "Percent Positive Sentiment"}, norm=divnorm)
    ax.axis('off')
    ax.set_title(" 11/" + str(day["Date"].iloc[0]), fontdict={"fontsize": "12", "fontweight": "3"})

    # save to an image file
    fig.savefig("map_export" + str(day['Date'].iloc[0]) + ".png", dpi=300)
