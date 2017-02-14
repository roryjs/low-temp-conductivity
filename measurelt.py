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
import argparse

# Connect to devices
ITC = MercuryITC('COM3') # PI USB-to-serial connection COM3
t = ITC.modules[0] # module 0 is temperature board
#h = ITC.modules[1] # module 1 is heater power board

PSU = TenmaPSU('COM4') # USK-K-R-COM USB-to-serial connection COM4, must be connected via USB hub
#print(PSU.GetIdentity()) # Prints PSU device identity string to terminal


def get_args():
    parser = argparse.ArgumentParser(description='Do some measurements.')
    parser.add_argument('-n', '--npts', type=int, required=True, default=10, help='')
    parser.add_argument('-s', '--savename', type=str, required=True, default='output.txt',  help='')
    parser.add_argument('-t', '--temp', type=int, required=True, default=77, help='Init temp')
    parser.add_argument('-u', '--tempstep', type=int, required=True, default=5, help='Temp step')

    return parser.parse_args()


def set_temp(temp):
    t.tset = temp
    reading = t.tset

    # read in the temperature setpoint. t.temp returns a tuple containing the latest
    # temperature reading(float) as element 0 and unit(string) as element 1
    print('Temperature set to {} {}'.format(reading[0], reading[1]))  # print to screen

    sleep(60 * 15)


def set_psu():
    # National Instruments GPIB-USB-HS GPIB interface
    Vdmm = K2000(16, 0)  # GPIB adaptor gpib0, device address 16
    Vdmm.write(":SENS:FUNC 'VOLT:DC'")  # configure to dc voltage
    Idmm = K2000(26, 0)  # GPIB adaptor gpib0, device address 26
    Idmm.write(":SENS:FUNC 'CURR:DC'")  # configure to dc current

    PSU.SetCurrent = 0.01 #A
    # write the PSU current setpoint (float, in Ampere units)
    print('PSU current output set to {} A'.format(PSU.SetCurrent))
    # read back PSU current setpoint value and print to terminal

    PSU.SetVoltage = 0.5  # V
    # write the PSU current setpoint (float, in Ampere units)
    print('PSU voltage output set to {} A'.format(PSU.SetVoltage))
    # read back PSU current setpoint value and print to terminal


def iterate_temp(npts, temp, tstep, savename):
    # initialise data arrays
    T = numpy.zeros(npts)
    V = numpy.zeros(npts)
    I = numpy.zeros(npts)
    R = numpy.zeros(npts)


    # loop to take repeated readings
    for p in range(npts):
        set_temp(temp)

        T[p] = t.temp[0]
        # t.temp returns a tuple containing the latest temperature reading (float)
        # as element 0 and unit(string) as element 1
        V[p] = Vdmm.reading # *dmm.reading returns latest reading from *dmm (float, in Volt or Ampere units)
        I[p] = Idmm.reading
        R[p] = V[p] / I[p] # calculate resistance - note the __future__ division import...
        print(p, T[p], V[p], I[p]) # print to screen

        # plot a graph
        pylab.figure()
        pylab.plot(T, '-k', marker='x')
        pylab.plot(V, '-b', marker='x')
        pylab.plot(I, '-r', marker='x')
        pylab.plot(R, '-r', marker='o')
        pylab.show()

        temp += tstep

    if not (savename == None):
        numpy.savetxt(savename, (T, V, I))  # save data to file


if __name__ == "__main__":
    args = get_args()

    set_psu()

    iterate_temp(args.npts, args.temp, args.tstep, args.savename)

    PSU.OutputOff  # Turn off PSU output

    # Disconnect from instruments
    PSU.close()
    ITC.close()
