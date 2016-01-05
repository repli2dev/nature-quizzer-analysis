# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot

matplotlib.rc('font', family='Arial')

def f1(prob):
    return -23*prob+25

def f2(prob):
    return 20/(prob+0.57)-10.5

t = np.arange(0, 1.1, 0.1)

pyplot.xticks([0, 0.5, 1])

y = np.array([2,14])
pyplot.yticks([2,8,10,13,14])

pyplot.plot(t, f2(t), 'b-', label = u'Současná funkce', )
pyplot.plot(t, f2(t), 'bo')
ax = pyplot.subplot()
pyplot.plot(t, f1(t), 'r-', t, f1(t), 'ro', label = u'Původní funkce')

axes = pyplot.gca()
axes.set_ylim([0, 26])

handles, labels = ax.get_legend_handles_labels()
display = (0,1)
ax.legend([handle for i,handle in enumerate(handles) if i in display], [label for i,label in enumerate(labels) if i in display], loc='upper center')

pyplot.ylabel(u'Taxonomická vzdálenost')
pyplot.xlabel(u'Pravděpodobnost úspěchu studenta na dané otázce')
pyplot.grid(axis='y', linestyle='--')
pyplot.grid(axis='x', linestyle='--')
pyplot.show()