import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import sys
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

mode = sys.argv[1]

if mode == "M":
    df0 = pd.read_json('MykyData/StreamingHistory0.json')
    df1 = pd.read_json('MykyData/StreamingHistory1.json')
    df_all = pd.concat([df0, df1], axis=0)
    CACHE = '.cache'
else:
    df0 = pd.read_json('SafiData/StreamingHistory0.json')
    df1 = pd.read_json('SafiData/StreamingHistory1.json')
    df2 = pd.read_json('SafiData/StreamingHistory2.json')
    df3 = pd.read_json('SafiData/StreamingHistory3.json')
    df_all = pd.concat([df0, df1, df2, df3], axis=0)
    CACHE = '.spotipyoauthcache'

# df0 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory0.json')
# df1 = pd.read_json('~/Documents/CS 439/Final Project/MyAccData/StreamingHistory1.json')
#
# df0['week'] = pd.to_datetime(df0['endTime']).dt.isocalendar().week
# df1['week'] = pd.to_datetime(df1['endTime']).dt.isocalendar().week
# df0['day'] = pd.to_datetime(df0['endTime']).dt.dayofweek
# df1['day'] = pd.to_datetime(df1['endTime']).dt.dayofweek
# df0['hour'] = pd.to_datetime(df0['endTime']).dt.hour
# df1['hour'] = pd.to_datetime(df1['endTime']).dt.hour
#
# df = pd.concat([df0, df1], axis=0)
df_all['week'] = pd.to_datetime(df_all['endTime']).dt.isocalendar().week
df_all['day'] = pd.to_datetime(df_all['endTime']).dt.dayofweek
df_all['hour'] = pd.to_datetime(df_all['endTime']).dt.hour

df = df_all

# print(df)


def ms_to_sec(x):
    total_sec = int(x / 1000)
    minutes = int(total_sec / 60)
    return minutes


class Window(QDialog):

    # constructor
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)

        layout = QVBoxLayout()

        self.radioButton_day = QRadioButton("By Day")
        self.radioButton_day.toggled.connect(self.daySelected)

        self.radioButton_hour = QRadioButton("By Hour")
        self.radioButton_hour.toggled.connect(self.hourSelected)

        self.figure = plt.figure()

        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self)

        self.radioButton_day.setChecked(True)

        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)

        grid = QGridLayout()  # 1 x 2
        grid.addWidget(self.radioButton_day, 0, 0)
        grid.addWidget(self.radioButton_hour, 0, 1)
        layout.addLayout(grid)
        self.setLayout(layout)

    def daySelected(self):
        self.figure.clear()

        sum_df = df.groupby(['week', 'day']).sum(numeric_only=True)
        sum_df['minutes'] = sum_df['msPlayed'].apply(ms_to_sec)
        # print(sum_df)

        df_wide = sum_df.pivot_table(index='day', columns='week', values='minutes')
        df_wide = df_wide.fillna(0)
        # print(df_wide)

        ax = self.figure.add_subplot(111)

        sns.heatmap(df_wide, cmap="Reds", cbar_kws={'label': 'Minutes'}, ax=ax)
        plt.title("Listening Activity")
        ax.set_yticklabels(['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
        ax.set(ylabel=None)
        self.canvas.draw()

    def hourSelected(self):
        self.figure.clear()

        sum_df = df.groupby(['day', 'hour']).sum(numeric_only=True)
        sum_df['minutes'] = sum_df['msPlayed'].apply(ms_to_sec)
        # print(sum_df)

        df_wide = sum_df.pivot_table(index='hour', columns='day', values='minutes')
        df_wide = df_wide.fillna(0)
        # print(df_wide)

        ax = self.figure.add_subplot(111)
        sns.heatmap(df_wide, cmap="Reds", cbar_kws={'label': 'Minutes'}, ax=ax)
        plt.title("Listening Activity")
        ax.set_xticklabels(['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun'])
        ax.set(xlabel=None)
        self.canvas.draw()

def run():
    # creating apyqt5 application
    app = QApplication(sys.argv)

    # creating a window object
    main = Window()
    main.resize(900, 900)

    # showing the window
    main.show()

    # loop
    sys.exit(app.exec_())


# driver code
if __name__ == '__main__':
    run()
