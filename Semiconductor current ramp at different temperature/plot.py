import numpy
import matplotlib.pyplot as pyplot
from scipy.optimize import curve_fit
import matplotlib.cm

pyplot.figure()
N_POINTS = 20
cols = ['b', 'g', 'r', 'c']
for a,i in enumerate([80,100]):
    (T, V, I, ti, ti_V, voltages) = numpy.loadtxt('semi-v-ramp-0.95-1.1-t-' + str(i) + '.txt')
    ti_V = numpy.trim_zeros(ti_V, 'b')
    voltages = numpy.trim_zeros(voltages, 'b')
    V = numpy.abs(V)

    av_V = numpy.zeros(16)
    av_I = numpy.zeros(16)
    av_T = numpy.zeros(16)

    for j in range(60, 1020, 60):
        av_V[j / 60 - 1] = numpy.abs(numpy.average(V[j - N_POINTS:j]))
        av_I[j / 60 - 1] = numpy.average(I[j - N_POINTS:j])
        av_T[j / 60 - 1] = numpy.average(T[j - N_POINTS:j])

    x = numpy.abs(V)
    y = I

    def exponenial_func(x, a, b):
        return a*numpy.exp(b*x) - a

    pyplot.xlabel('Voltage, V (V)')
    pyplot.ylabel('Current, I (A)')

    popt, pcov = curve_fit(exponenial_func, x, y, p0=(10**(-25), 47), maxfev=10000)

    print 'av temp'
    print 'mean: ' + str(numpy.mean(av_T))
    print 'st dev: ' + str(numpy.std(av_T))
    print 't = ' + str(numpy.mean(av_T)) + ' +/- ' + str(numpy.max(numpy.max(av_T)-numpy.mean(av_T), numpy.mean(av_T) - numpy.min(av_T)))
    print 'ideality factor:'
    print (1.60217646e-19 / 1.3806503e-23)/(numpy.mean(av_T) * popt[1])
    print ''
    xx = numpy.linspace(0.92,1.07,100)
    yy = exponenial_func(xx, *popt)

    pyplot.plot(av_V, av_I, 'o' + cols[a])
    pyplot.plot(xx, yy, '-' + cols[a], label=str(i) + 'K')
    #y = 0.3*10**(-25)*(numpy.e**((x * 1.60217662 * 10**(-19))/(2.95*1.38*10**(-23)*80))-1)


pyplot.axis([0.92,1.08, 0.0,0.004])
pyplot.legend(loc=2)
ax = pyplot.gca()
ax.set_autoscale_on(False)






pyplot.figure()

for a,i in enumerate([90,110,120,130]):
    (T, V, I, ti, ti_V, voltages) = numpy.loadtxt('semi-v-ramp-0.95-1.1-t-' + str(i) + '.txt')
    ti_V = numpy.trim_zeros(ti_V, 'b')
    voltages = numpy.trim_zeros(voltages, 'b')
    V = numpy.abs(V)

    av_V = numpy.zeros(16)
    av_I = numpy.zeros(16)
    av_T = numpy.zeros(16)

    for j in range(60, 1020, 60):
        av_V[j / 60 - 1] = numpy.abs(numpy.average(V[j - N_POINTS:j]))
        av_I[j / 60 - 1] = numpy.average(I[j - N_POINTS:j])
        av_T[j / 60 - 1] = numpy.average(T[j - N_POINTS:j])



    x = numpy.abs(V)
    y = I

    def exponenial_func(x, a, b):
        return a*numpy.exp(b*x) - a

    pyplot.xlabel('Voltage, V (V)')
    pyplot.ylabel('Current, I (A)')

    popt, pcov = curve_fit(exponenial_func, x, y, p0=(10**(-25), 47), maxfev=10000)

    print 'av temp'
    print 'mean: ' + str(numpy.mean(av_T))
    print 'st dev: ' + str(numpy.std(av_T))
    print 't = ' + str(numpy.mean(av_T)) + ' +/- ' + str(numpy.max(numpy.max(av_T)-numpy.mean(av_T), numpy.mean(av_T) - numpy.min(av_T)))
    print 'ideality factor:'
    print (1.60217646e-19 / 1.3806503e-23)/(numpy.mean(av_T) * popt[1])
    print ''
    xx = numpy.linspace(0.92,1.08,100)
    yy = exponenial_func(xx, *popt)

    pyplot.plot(av_V, av_I, 'o' + cols[a])
    pyplot.plot(xx, yy, '-' + cols[a], label=str(i) + 'K')
    #y = 0.3*10**(-25)*(numpy.e**((x * 1.60217662 * 10**(-19))/(2.95*1.38*10**(-23)*80))-1)


pyplot.axis([0.92,1.08, 0.0,0.005])
pyplot.legend(loc=2)
ax = pyplot.gca()
ax.set_autoscale_on(False)














pyplot.show()
