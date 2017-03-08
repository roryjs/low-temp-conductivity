import numpy
import matplotlib.pyplot as pyplot
'''
(T, V, I, ti, ti_V, voltages) = numpy.loadtxt('v-ramp-0.95-1.1-t-100.txt')
ti_V = numpy.trim_zeros(ti_V, 'b')    
voltages = numpy.trim_zeros(voltages, 'b')

ramp_index = []
for ti_ramp_pt in ti_V:
    for i,time in enumerate(ti):
        if time > ti_ramp_pt:
            ramp_index.append(i)
            break

  
av_voltages = []                   
av_currents = []  
for i in ramp_index:
    av_voltages.append(numpy.abs(numpy.average(V[i-10:i])))
    av_currents.append(numpy.average(I[i-10:i]))
print av_voltages
    
(T2, V2, I2, ti2, ti_V2, voltages2) = numpy.loadtxt('v-ramp-0.95-1.1.txt')
ti_V2 = numpy.trim_zeros(ti_V2, 'b')    
voltages2 = numpy.trim_zeros(voltages2, 'b')

ramp_index2 = []
for ti_ramp_pt2 in ti_V2:
    for i2,time2 in enumerate(ti2):
        if time2 > ti_ramp_pt2:
            ramp_index2.append(i2)
            break

av_voltages2 = []                   
av_currents2 = []  
for i in ramp_index2:
    av_voltages2.append(numpy.abs(numpy.average(V2[i-10:i])))
    av_currents2.append(numpy.average(I2[i-10:i]))
print av_voltages2'''
(T, V, I, ti, ti_I, currents) = numpy.loadtxt('super-i-ramp-0.2-2.6.txt')
ti_I = numpy.trim_zeros(ti_I, 'b')
currents = numpy.trim_zeros(currents, 'b')

ramp_index = []
for ti_ramp_pt in ti_I:
    for i,time in enumerate(ti):
        if time > ti_ramp_pt:
            ramp_index.append(i)
            break

  
av_voltages = []                   
av_currents = []  
for i in ramp_index:
    av_voltages.append(numpy.abs(numpy.average(V[i-10:i])))
    av_currents.append(numpy.average(I[i-10:i]))
print av_voltages
#print temps
#print ti_temp

'''(T, V, I, ti, ti_T, temps) = numpy.loadtxt('t-ramp-80-180.txt')
ti_T = numpy.trim_zeros(ti_T)
temps = numpy.trim_zeros(temps)'''

pyplot.figure()
pyplot.plot(av_currents, av_voltages)
#pyplot.plot(av_voltages2, av_currents2)
#pyplot.plot(I, V)
#pyplot.plot(ti, V/I)
#pylab.plot(ti, V)
#pyplot.plot(I, V)

pyplot.show()
