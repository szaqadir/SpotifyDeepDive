import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

df0 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory0.json')
df1 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory1.json')

df0['week'] = pd.to_datetime(df0['endTime']).dt.isocalendar().week
df1['week'] = pd.to_datetime(df1['endTime']).dt.isocalendar().week
df0['day'] = pd.to_datetime(df0['endTime']).dt.dayofweek
df1['day'] = pd.to_datetime(df1['endTime']).dt.dayofweek

df = pd.concat([df0, df1], axis=0)


def ms_to_sec(x):
    total_sec = int(x / 1000)
    minutes = int(total_sec / 60)
    return minutes


sum_df = df.groupby(['week', 'day']).sum(numeric_only=True)
sum_df['minutes'] = sum_df['msPlayed'].apply(ms_to_sec)
print(sum_df)

df_wide = sum_df.pivot_table(index='day', columns='week', values='minutes')
df_wide = df_wide.fillna(0)
print(df_wide)

fig, ax = plt.subplots(figsize=(15, 4))
sns.heatmap(df_wide, cmap="Reds", cbar_kws={'label': 'Minutes'}, ax=ax)
ax.set_yticklabels(['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
plt.show()

# hover tool tip should show: top 3/5 artists/songs from that day, as well as the date!!!
