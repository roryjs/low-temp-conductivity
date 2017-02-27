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


# new code to write txt

numpy.savetxt('output3.txt', (T, V, I, ti))

with open('output3.txt') as f:
    data = f.readlines()

print data