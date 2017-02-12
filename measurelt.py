# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 13:10:15 2016

@author: Aidan Hindmarch

Example script to run low temperature conductivity experiment.

Controls: 
    Keithley 2000 series DMM
    Oxford Instruments Mercury iTC temperature controller
    Tenma 72-2550 PSU

"""
from __future__ import print_function, division
from level2labs.lowtemperature import K2000, MercuryITC, TenmaPSU
from time import sleep

import sys
import numpy
import pylab

# Get required number of points and output filename from commandline
#npts = 10
npts = int(sys.argv[1])
#savename = None
savename = sys.argv[2]

# Connect to devices
ITC = MercuryITC('COM3') # PI USB-to-serial connection COM3
t = ITC.modules[0] # module 0 is temperature board 
#h = ITC.modules[1] # module 1 is heater power board

PSU = TenmaPSU('COM4') # USK-K-R-COM USB-to-serial connection COM4, must be connected via USB hub
#print(PSU.GetIdentity()) # Prints PSU device identity string to terminal

#National Instruments GPIB-USB-HS GPIB interface
Vdmm = K2000(16,0) # GPIB adaptor gpib0, device address 16
Vdmm.write(":SENS:FUNC 'VOLT:DC'") # configure to dc voltage
Idmm = K2000(26,0) # GPIB adaptor gpib0, device address 26
Idmm.write(":SENS:FUNC 'CURR:DC'") # configure to dc current

temp = t.tset 
# read in the temperature setpoint. t.temp returns a tuple containing the latest 
# temperature reading(float) as element 0 and unit(string) as element 1
print('Temperature set to {} {}'.format(temp[0],temp[1])) # print to screen

PSU.SetCurrent=0.01 #A
# write the PSU current setpoint (float, in Ampere units)
print('PSU current output set to {} A'.format(PSU.SetCurrent))
# read back PSU current setpoint value and print to terminal


# initialise data arrays
T = numpy.zeros(npts)
V = numpy.zeros(npts)
I = numpy.zeros(npts)
#R = numpy.zeros(npts)

# loop to take repeated readings
for p in range(npts):
    #PSU.SetCurrent=0.002*p #A - current ramp
	#	or
    #PSU.SetVoltage=0.05*p #V - voltage ramp

    sleep(0.1) # pause before taking readings
    T[p]=t.temp[0] 
    # t.temp returns a tuple containing the latest temperature reading (float) 
    # as element 0 and unit(string) as element 1
    V[p]=Vdmm.reading # *dmm.reading returns latest reading from *dmm (float, in Volt or Ampere units)
    I[p]=Idmm.reading
    #R[p]=V[p]/I[p] # calculate resistance - note the __future__ division import...
    print(p, T[p], V[p], I[p]) # print to screen
 
PSU.OutputOff	# Turn off PSU output

if not (savename==None):      
    numpy.savetxt(savename, (T,V,I)) # save data to file

#t.tset = 100.0 # set temperture setpoint on ITC to next required value
temp=t.tset # read in the temperature setpoint
print('Temperature set to {} {}'.format(temp[0],temp[1])) # print to screen

#Disconnect from instruments
PSU.close()
ITC.close()


# plot a graph
pylab.figure()
#pylab.plot(T, '-k', marker='x')
pylab.plot(V, '-b', marker='x')
#pylab.plot(I, '-r', marker='x')
#pylab.plot(R, '-r', marker='o')
pylab.show()
