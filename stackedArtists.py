import mplcursors as mplcursors
import pandas as pd
import matplotlib.pyplot as plt
import calendar

df0 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory0.json')
df1 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory1.json')

df0['month'] = pd.to_datetime(df0['endTime']).dt.month
df1['month'] = pd.to_datetime(df1['endTime']).dt.month

df_all = pd.concat([df0, df1], axis=0)

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
vert_offset = 1.0
ax.legend(bbox_to_anchor=(horiz_offset, vert_offset))
ax.set_ylabel("Minutes Played")

cursor = mplcursors.cursor(hover=mplcursors.HoverMode.Transient)


@cursor.connect("add")
def on_add(sel):
    sel.annotation.set_text(
        '--- {} ---\n{}\n{} minutes'.format(calendar.month_name[sel.index + 1], sel.artist.get_label(),
                                            table.iloc[sel.index][sel.artist.get_label()]))
    sel.annotation.get_bbox_patch().set(fc="white")
    sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=.5)

plt.title("Top Artists throughout the Year")
plt.tight_layout()
plt.show()

# import filename WORKS WOOOOOOO
