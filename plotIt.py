import numpy
import pylab
import os

__location__ = os.path.realpath(
    os.path.join(os.getcwd(), os.path.dirname(__file__)))

txt = open(os.path.join(__location__, 'output2.txt'));
(T, V, I, ti) = numpy.loadtxt(txt)
pylab.figure()
pylab.plot(T, V/I)
#pylab.plot(ti, V)
#pylab.plot(ti, I)

pylab.show()
