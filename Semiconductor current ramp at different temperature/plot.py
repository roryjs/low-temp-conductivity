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

    for c in range(0,2):
        if c==0:
            if i == 80:
                x = av_V[:8]
                y = numpy.log(av_I[:8])
            elif i == 100:
                x = av_V[:5]
                y = numpy.log(av_I[:5])
        if c==1:
            if i == 80:
                x = av_V[-7:]
                y = numpy.log(av_I[-7:])
            elif i == 100:
                x = av_V[-10:]
                y = numpy.log(av_I[-10:])

        def exponenial_func(x, a, b):
            return numpy.log(a) + b * x

        pyplot.xlabel('Voltage, V (V)')
        pyplot.ylabel('Current, I (A)')

        popt, pcov = curve_fit(exponenial_func, x, y, p0=(1e-5, 1), maxfev=100000)

        xx = numpy.linspace(0.92, 1.08, 100)
        yy = exponenial_func(xx, *popt)

        #pyplot.plot(x,y)
        if c==0:
            pyplot.plot(xx, yy, '-' + cols[a], label=str(i) + 'K')
        else:
            pyplot.plot(xx, yy, '-' + cols[a])
        grad = popt[1]
        grad_err = numpy.sqrt(numpy.diag(pcov))[1]
        print 'grad = ' + str(grad)
        print 'err in grad = ' + str(grad_err)
        id_fac = (1.60217646e-19 / 1.3806503e-23)/(numpy.mean(av_T) * popt[1])
        id_fac_error = id_fac * (grad_err/grad)
        print 'ideality factor: ' + str(id_fac) + ' \pm ' + str(id_fac_error)
        sat_cur = popt[0]
        sat_cur_err = numpy.sqrt(numpy.diag(pcov))[0]
        print 'sat current: ' + str(sat_cur) + ' \pm ' + str(sat_cur_err)


    pyplot.plot(av_V, numpy.log(av_I), 'o' + cols[a])

    print 'av temp'
    print 'mean: ' + str(numpy.mean(av_T))
    print 'st dev: ' + str(numpy.std(av_T))
    print 't = ' + str(numpy.mean(av_T)) + ' \pm ' + str(numpy.max(numpy.max(av_T)-numpy.mean(av_T), numpy.mean(av_T) - numpy.min(av_T)))

    print ''
    print ''
    print ''

    #y = 0.3*10**(-25)*(numpy.e**((x * 1.60217662 * 10**(-19))/(2.95*1.38*10**(-23)*80))-1)


pyplot.axis([0.92,1.08, -13,-5])
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

    for c in range(0,2):
        if c==0:
            if i == 90:
                x = av_V[1:8]
                y = numpy.log(av_I[1:8])
            elif i == 110:
                x = av_V[:5]
                y = numpy.log(av_I[:5])
            if i == 120:
                x = av_V[:5]
                y = numpy.log(av_I[:5])
            elif i == 130:
                x = av_V[:7]
                y = numpy.log(av_I[:7])

        if c==1:
            if i == 90:
                x = av_V[-5:]
                y = numpy.log(av_I[-5:])
            elif i == 110:
                x = av_V[-7:]
                y = numpy.log(av_I[-7:])
            if i == 120:
                x = av_V[-8:]
                y = numpy.log(av_I[-8:])
            elif i == 130:
                x = av_V[-5:]
                y = numpy.log(av_I[-5:])

        def exponenial_func(x, a, b):
            return numpy.log(a) + b * x

        pyplot.xlabel('Voltage, V (V)')
        pyplot.ylabel('Current, I (A)')

        popt, pcov = curve_fit(exponenial_func, x, y, p0=(1e-5, 1), maxfev=100000)

        xx = numpy.linspace(0.92, 1.08, 100)
        yy = exponenial_func(xx, *popt)

        #pyplot.plot(x,y)
        if c==0:
            pyplot.plot(xx, yy, '-' + cols[a], label=str(i) + 'K')
        else:
            pyplot.plot(xx, yy, '-' + cols[a])
        grad = popt[1]
        grad_err = numpy.sqrt(numpy.diag(pcov))[1]
        print 'grad = ' + str(grad)
        print 'err in grad = ' + str(grad_err)
        id_fac = (1.60217646e-19 / 1.3806503e-23)/(numpy.mean(av_T) * popt[1])
        id_fac_error = id_fac * (grad_err/grad)
        print 'ideality factor: ' + str(id_fac) + ' \pm ' + str(id_fac_error)
        sat_cur = popt[0]
        sat_cur_err = numpy.sqrt(numpy.diag(pcov))[0]
        print 'sat current: ' + str(sat_cur) + ' \pm ' + str(sat_cur_err)

    pyplot.plot(av_V, numpy.log(av_I), 'o' + cols[a])

    print 'av temp'
    print 'mean: ' + str(numpy.mean(av_T))
    print 'st dev: ' + str(numpy.std(av_T))
    print 't = ' + str(numpy.mean(av_T)) + ' \pm ' + str(numpy.max(numpy.max(av_T)-numpy.mean(av_T), numpy.mean(av_T) - numpy.min(av_T)))

    print ''
    print ''
    print ''

    #y = 0.3*10**(-25)*(numpy.e**((x * 1.60217662 * 10**(-19))/(2.95*1.38*10**(-23)*80))-1)


#pyplot.axis([0.92,1.08, 0.0,0.005])
pyplot.legend(loc=2)
ax = pyplot.gca()
ax.set_autoscale_on(False)









pyplot.show()
