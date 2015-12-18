# -*- coding: utf-8 -*-

import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot

matplotlib.rc('font', family='Arial')

def f(prob):
    return np.clip(20/(prob+0.57)-10.5, 2, None)

t = np.arange(-0.5, 1.5, 0.1)

x = np.array([0.5])
pyplot.xticks(np.arange(t.min(), t.max(), 0.5))

y = np.array([2,9])
pyplot.yticks(np.arange(y.min(), y.max(), 6))

pyplot.plot(t, f(t), 'k', t, f(t), 'bo')

axes = pyplot.gca()
axes.set_ylim([0, 26])

pyplot.ylabel(u'Taxonomická vzdálenost')
pyplot.xlabel(u'Pravděpodobnost úspěchu studenta na dané otázce')
pyplot.grid(axis='y', linestyle='--')
pyplot.grid(axis='x', linestyle='--')
pyplot.show()