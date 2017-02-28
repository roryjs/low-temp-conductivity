import numpy
import matplotlib.pyplot as pyplot
from numpy import array as array
import os


(T, V, I, ti) = numpy.loadtxt('output3.txt')

pyplot.figure()
pyplot.plot(T, V/I)
#pylab.plot(ti, V)
#pylab.plot(ti, I)

pyplot.show()
