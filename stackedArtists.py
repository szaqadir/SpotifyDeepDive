import pandas as pd
import matplotlib.pyplot as plt

df0 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory0.json')
df1 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory1.json')

print(df0)
print(df1)

df0['month'] = pd.to_datetime(df0['endTime']).dt.month
df1['month'] = pd.to_datetime(df1['endTime']).dt.month

df_all = pd.concat([df0, df1], axis=0)

print(df_all)

groups = df_all.groupby(['artistName', 'month'])

list = []
for key, item in groups:
    group = groups.get_group(key)
    ms_sum = groups.get_group(key)['msPlayed'].sum()
    total_sec = int(ms_sum / 1000)
    minutes = int(total_sec / 60)
    list.append([group.iloc[0]['artistName'], group.iloc[0]['month'], minutes])

df = pd.DataFrame(list, columns=['artistName', 'month', 'min_played'])
df = df.sort_values(by=['month', 'min_played'], ascending=[True, False]).groupby('month', as_index=False).nth[:5]
table = pd.pivot_table(df, values='min_played', index='month', columns='artistName', fill_value=0).reset_index()

ax = table.plot(x='month', kind='bar', stacked=True, colormap="Spectral")

horiz_offset = 1.03
vert_offset = 1.
ax.legend(bbox_to_anchor=(horiz_offset, vert_offset))

plt.tight_layout()
plt.show()