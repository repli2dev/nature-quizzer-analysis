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
with open('../data/processed/success_rate_per_day.csv', 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='"')
    for row in reader:
        data.append(row)

x = [datetime.datetime.strptime(date, '%Y-%m-%d') for date,_,_ in data]
y = [all for _,all,_ in data]
z = [correct for _,_,correct in data]

a = [float(correct)/float(all)*100 for _,all,correct in data]

# Confidence intervals
# Adapted from http://graphpad.com/guides/prism/6/statistics/index.htm?how_to_compute_the_95_ci_of_a_proportion.htm
p = [((float(correct)+0.5*1.96**2)/(float(all)+1.96**2), float(all), float(correct)) for _,all,correct in data]
w = [100*(1.96 * math.sqrt( (p1 *(1-p1))/(n+1.96**2) )) for p1, n, correct in p]

#for i in range(len(data)):
#    print data[i], w[i]

pyplot.ylabel(u'Počet odpovědí')
pyplot.xlabel(u'Datum')
pyplot.gcf().axes[0].xaxis.set_major_formatter(formatter)
pyplot.gcf().autofmt_xdate()

ax = pyplot.subplot()
p1 = pyplot.plot(x,y, label=u'Všechny odpovědi')

pyplot.subplot()
pyplot.plot(x,z, 'r', label=u'Správné odpovědi')

handles, labels = ax.get_legend_handles_labels()
display = (0,1)
ax.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='upper center')

pyplot.figure(2)
pyplot.ylabel(u'Správných odpovědí v %')
pyplot.xlabel(u'Datum')
pyplot.gcf().axes[0].xaxis.set_major_formatter(formatter)
pyplot.gcf().autofmt_xdate()
axes = pyplot.gca()
axes.set_ylim([0, 100])
pyplot.errorbar(x, a, yerr=w, ecolor='k')

temp_all = 0
temp_correct = 0
for _,all, correct in data:
    temp_all += float(all)
    temp_correct += float(correct)

print temp_correct, temp_all, float(temp_correct)/temp_all

# TODO: spolehlivostní intervaly

pyplot.show()