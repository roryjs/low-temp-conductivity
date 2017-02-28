import numpy
import matplotlib.pyplot as pyplot
from numpy import array as array
import os


(T, V, I, ti, ti_temp, temps) = numpy.loadtxt('output2.txt')
ti_temp = numpy.trim_zeros(ti_temp)
temps = numpy.trim_zeros(temps)

#(T, V, I, ti, ti_I, currents) = numpy.loadtxt('output2.txt')
#ti_I = numpy.trim_zeros(ti_I)
#currents = numpy.trim_zeros(currents)

pyplot.figure()
pyplot.plot(ti, T)
pyplot.plot(ti, V/I)
#pylab.plot(ti, V)
#pylab.plot(ti, I)

pyplot.show()
