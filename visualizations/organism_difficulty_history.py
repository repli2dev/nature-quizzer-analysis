# -*- coding: utf-8 -*-

import datetime
import csv
import math
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.dates as dates

matplotlib.rc('font', family='Arial')
formatter = dates.DateFormatter('%d. %m. %Y')

data = []
with open('../data/processed/organism_difficulty_history.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        data.append(list(row))


max_length = max(len(data[0]), len(data[1]), len(data[2]), len(data[3]))+1
for i in range(4):
    for _ in range(0, max_length - len(data[i])):
        data[i].append(None)

x = range(0, max_length)

pyplot.ylabel(u'Odhad obtížnosti druhu organismu')
pyplot.xlabel(u'Počet odpovědí')

ax = pyplot.subplot()
pyplot.plot(x,data[0], label=u'krysa obecná')
pyplot.plot(x,data[1], label=u'potkan')
pyplot.plot(x,data[2], label=u'plch zahradní')
pyplot.plot(x,data[3], label=u'skřivan polní')
pyplot.axis([0, 180, -1.5, 2])
pyplot.grid(axis='y', linestyle='--')
pyplot.grid(axis='x', linestyle='--')

handles, labels = ax.get_legend_handles_labels()
display = (0,1,2,3)
ax.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='upper right')

pyplot.show()