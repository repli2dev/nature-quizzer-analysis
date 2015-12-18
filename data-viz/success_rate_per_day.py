# -*- coding: utf-8 -*-

import datetime
import csv
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.dates as dates

matplotlib.rc('font', family='Arial')
formatter = dates.DateFormatter('%d. %m. %Y')

data = []
with open('../data/success_rate_per_day.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        data.append(row)

x = [datetime.datetime.strptime(date, '%Y-%m-%d') for date,_,_ in data]
y = [all for _,all,_ in data]
z = [correct for _,_,correct in data]

a = [float(correct)/float(all)*100 for _,all,correct in data]

pyplot.ylabel(u'Počet odpovědí')
pyplot.xlabel(u'Datum')
pyplot.gcf().axes[0].xaxis.set_major_formatter(formatter)
pyplot.gcf().autofmt_xdate()

ax = pyplot.subplot()
p1 = pyplot.plot(x,y, label='All answers')

pyplot.subplot()
pyplot.plot(x,z, 'r', label='Correct answers')

handles, labels = ax.get_legend_handles_labels()
display = (0,1)
ax.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='upper center')

pyplot.figure(2)
pyplot.ylabel(u'Správných odpovědí')
pyplot.xlabel(u'Datum')
pyplot.gcf().axes[0].xaxis.set_major_formatter(formatter)
pyplot.gcf().autofmt_xdate()
axes = pyplot.gca()
axes.set_ylim([0, 100])
pyplot.plot(x,a)

# TODO: spolehlivostní intervaly

pyplot.show()