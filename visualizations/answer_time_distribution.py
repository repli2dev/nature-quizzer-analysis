# -*- coding: utf-8 -*-

import datetime
import csv
import math
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.dates as dates

matplotlib.rc('font', family='Arial')
formatter = dates.DateFormatter('%d. %m. %Y')

data1 = {}
data2 = {}
with open('../data/processed/answer_time.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        if int(row[0]) == 1:
            if not (int(row[1])/1000) in data1:
                data1[int(row[1])/1000] = 0
            data1[int(row[1])/1000] += 1
        else:
            if not (int(row[1])/1000) in data2:
                data2[int(row[1])/1000] = 0
            data2[int(row[1])/1000] += 1

x = range(0,max(data1.keys())+1)

y1 = [0 for _ in range (max(data1.keys())+1)]
for key, value in data1.items():
    y1[key] = value

y2 = [0 for _ in range (max(data1.keys())+1)]
for key, value in data2.items():
    y2[key] = value


pyplot.ylabel(u'Počet odpovědí')
pyplot.xlabel(u'Čas (v sekundách)')
ax = pyplot.subplot()
pyplot.plot(x,y1, label=u'Otázky rozpoznání reprezentace')
ax = pyplot.subplot()
pyplot.plot(x,y2, label=u'Otázky rozpoznání obrázku')
pyplot.axis([0, 30 , 0, 400])

handles, labels = ax.get_legend_handles_labels()
display = (0,1)
ax.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='upper right')

pyplot.show()