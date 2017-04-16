import numpy
import matplotlib.pyplot as pyplot
from scipy.optimize import curve_fit

pyplot.figure()

id_fac = 1.5

def func(x, a, b):
    return a - b*x

(T, V, I, ti, ti_T, temps) = numpy.loadtxt('semi-t-ramp-80-180-v-1.1.txt')
ti_T = numpy.trim_zeros(ti_T, 'b')[1:]
temps = numpy.trim_zeros(temps, 'b')
V = numpy.abs(V)

av_V = numpy.zeros(21)
av_I = numpy.zeros(21)
av_T = numpy.zeros(21)
for i in range(600, 12601, 600):
    av_V[i/600 - 1] = numpy.abs(numpy.average(V[i - 100:i]))
    av_I[i/600 - 1] = numpy.average(I[i - 100:i])
    av_T[i / 600 - 1] = numpy.average(T[i - 100:i])


x = 1/av_T
y = numpy.log(av_I)
popt, pcov = curve_fit(func, x, y, p0=(1, 1), maxfev=100000)



xx = numpy.linspace(0.005, 0.013, 1000)
yy = func(xx, *popt)

pyplot.plot(x, y, 'o', xx, yy)
eg = (numpy.mean(av_V)) - popt[1] * 1.3806503e-23 * id_fac / 1.60217646e-19
print 'av V: ' + str(numpy.mean(av_V)) + ' \pm ' + str(numpy.max(numpy.max(av_V)-numpy.mean(av_V), numpy.mean(av_V) - numpy.min(av_V)))
print 'Eg: ' + str(eg) + ' \pm ' + str(numpy.sqrt(numpy.diag(pcov))[1])
#a,b = popt
#pyplot.plot(1/av_T, numpy.log(av_I))
pyplot.xlabel('1/T')
pyplot.ylabel('ln(I)')

pyplot.show()