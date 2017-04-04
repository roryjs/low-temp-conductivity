import numpy
import matplotlib.pyplot as pyplot

pyplot.figure()
V_all = []
I_all = []
for name in ['semi-rev-v-ramp-1-11.txt', 'semi-rev-v-ramp-11-12.txt', 'semi-rev-v-ramp-11.8-11.9.txt', 'semi-rev-v-ramp-11.89-11.93.txt' ,'semi-rev-v-ramp-11.93-12.txt', 'semi-rev-v-ramp-11.8-13.txt']:
    (T, V, I, ti, ti_V, voltages) = numpy.loadtxt(name)
    V = -numpy.absolute(V)
    I = -numpy.absolute(I)

    ti_V = numpy.trim_zeros(ti_V, 'b')
    voltages = numpy.trim_zeros(voltages, 'b')

    ramp_index = []
    for ti_ramp_pt in ti_V:
        for i, time in enumerate(ti):
            if time >= ti_ramp_pt or time == ti[-1]:
                ramp_index.append(i)
                break

    av_V = []
    av_I = []
    for i in ramp_index[1:]:
        av_V.append(numpy.average(V[i - 10:i]))
        av_I.append(numpy.average(I[i - 10:i]))

    if name == 'semi-rev-v-ramp-11.8-13.txt':
        av_V = av_V[3:]
        av_I = av_I[3:]
    elif name == 'semi-rev-v-ramp-11-12.txt':
        av_V = av_V[:-2]
        av_I = av_I[:-2]


    V_all.append(av_V)
    I_all.append(av_I)

V_all = numpy.concatenate(V_all)
I_all = numpy.concatenate(I_all)
Is = -numpy.mean(I_all[I_all > -1e-6])

print 'sat current: ' + str(Is)
pyplot.plot(V_all, I_all)

pyplot.show()