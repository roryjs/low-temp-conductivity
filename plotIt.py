import numpy
import matplotlib.pyplot as pyplot
from numpy import array as array
import os

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

txt = open(os.path.join(__location__, 'output.txt')).read()
(T, V, I, ti) = eval(txt)

pyplot.figure()
pyplot.plot(T, V/I)
#pylab.plot(ti, V)
#pylab.plot(ti, I)

pyplot. show()
