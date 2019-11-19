import geopandas as gpd
import pandas as pd
import matplotlib.pyplot as plt

# read in map shp file
shp_path = "ne_110m_admin_1_states_provinces/ne_110m_admin_1_states_provinces.shp"
map_df = gpd.read_file(shp_path)

df_by_day = []

# read states sentiment data
df = pd.read_csv('states_with_date.csv')
print(df.head())

for i in range(1,3):
    df_day = df[df['Date'] == i]
    df_day.columns = ["State", "Sent", "Date"]
    df_by_day.append(df_day)

count = 1
for day in df_by_day:
    print(day)
    # join map data with sentiment data
    merged = map_df.set_index('name').join(day.set_index("State"))

    # visualize the data
    variable = 'Sent'
    vmin, vmax = 120, 220
    fig, ax = plt.subplots(1, figsize=(10, 6))
    merged.plot(column=variable, cmap='BuGn', linewidth=0.8, ax=ax, edgecolor='0.8')
    ax.axis('off')
    ax.set_title("Tweet Sentiment", fontdict={"fontsize": "15", "fontweight": "3"})

    # save to an image file
    fig.savefig("map_export" + str(count) + ".png", dpi=300)
    count += 1
