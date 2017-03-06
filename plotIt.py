import numpy
import matplotlib.pyplot as pyplot

(T, V, I, ti, ti_temp, temps) = numpy.loadtxt('semi-80to140-5step.txt')
ti_temp = numpy.trim_zeros(ti_temp, 'b')
temps = numpy.trim_zeros(temps, 'b')
print temps
print ti_temp

#(T, V, I, ti, ti_I, currents) = numpy.loadtxt('output2.txt')
#ti_I = numpy.trim_zeros(ti_I)
#currents = numpy.trim_zeros(currents)

pyplot.figure()
pyplot.plot(ti, T)
#pyplot.plot(ti, V/I)
#pylab.plot(ti, V)
#pylab.plot(ti, I)

pyplot.show()
