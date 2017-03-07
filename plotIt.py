import numpy
import matplotlib.pyplot as pyplot

(T, V, I, ti, ti_V, voltages) = numpy.loadtxt('v-ramp-0.6-1.2.txt')
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
#(T, V, I, ti, ti_temp, temps) = numpy.loadtxt('semi-80to140-5step.txt')
#i_temp = numpy.trim_zeros(ti_temp, 'b')
#temps = numpy.trim_zeros(temps, 'b')
#print temps
#print ti_temp

#(T, V, I, ti, ti_I, currents) = numpy.loadtxt('output2.txt')
#ti_I = numpy.trim_zeros(ti_I)
#currents = numpy.trim_zeros(currents)

pyplot.figure()
pyplot.plot(av_voltages, av_currents)
#pyplot.plot(I, V)
#pyplot.plot(ti, V/I)
#pylab.plot(ti, V)
#pylab.plot(ti, I)

pyplot.show()
