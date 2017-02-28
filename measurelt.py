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
from time import sleep, time
from datetime import datetime

import sys
import numpy
import pylab
import argparse
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import passwords


# Connect to devices
ITC = MercuryITC('COM3')  # PI USB-to-serial connection COM3
t = ITC.modules[0]  # module 0 is temperature board
# h = ITC.modules[1] # module 1 is heater power board

PSU = TenmaPSU('COM4')  # USK-K-R-COM USB-to-serial connection COM4, must be connected via USB hub


# print(PSU.GetIdentity()) # Prints PSU device identity string to terminal


def get_args():
    parser = argparse.ArgumentParser(description='Do some measurements.')
    parser.add_argument('-n', '--npts', type=int, required=True, default=10, help='')
    parser.add_argument('-s', '--savename', type=str, required=True, default='output.txt', help='')
    parser.add_argument('-t', '--temp', type=int, required=True, default=77, help='Init temp')
    parser.add_argument('-u', '--tstep', type=int, required=True, default=5, help='Temp step')
    parser.add_argument('-w', '--wait', type=int, required=True, default=300, help='Wait time between readings.')

    return parser.parse_args()


def wait_to_cool(temp):
    t.tset = temp
    reading = t.tset

    # read in the temperature setpoint. t.temp returns a tuple containing the latest
    # temperature reading(float) as element 0 and unit(string) as element 1
    print('Temperature set to {} {}'.format(reading[0], reading[1]))  # print to screen

    while t.temp[0] - 1 > reading[0]:
        sleep(10)

    print('Waiting 5 mins... started at {}'.format(str(datetime.now())))
    
    sleep(5*60)


def set_temp(temp):
    t.tset = temp
    reading = t.tset

    # read in the temperature setpoint. t.temp returns a tuple containing the latest
    # temperature reading(float) as element 0 and unit(string) as element 1
    print('Temperature set to {} {}'.format(reading[0], reading[1]))  # print to screen


def set_psu():
    PSU.SetCurrent = 0.01  # A
    # write the PSU current setpoint (float, in Ampere units)
    print('PSU current output set to {} A'.format(PSU.SetCurrent))
    # read back PSU current setpoint value and print to terminal

    PSU.SetVoltage = 0.5  # V
    # write the PSU current setpoint (float, in Ampere units)
    print('PSU voltage output set to {} A'.format(PSU.SetVoltage))
    # read back PSU current setpoint value and print to terminal


def iterate_temp(npts, temp, tstep, savename, wait):
    # initialise data arrays
    T = numpy.zeros(npts * wait)
    V = numpy.zeros(npts * wait)
    I = numpy.zeros(npts * wait)
    ti = numpy.zeros(npts * wait)

    init_time = time()

    # loop to take repeated readings
    for p in range(npts):
        set_temp(temp)

        for l in range(wait):
            T[p * wait + l] = t.temp[0]
            # t.temp returns a tuple containing the latest temperature reading (float)
            # as element 0 and unit(string) as element 1
            V[p * wait + l] = Vdmm.reading  # *dmm.reading returns latest reading from *dmm (float, in Volt or Ampere units)
            I[p * wait + l] = Idmm.reading
            ti[p * wait + l] = time() - init_time

            sleep(1)

        temp += tstep

    if not (savename == None):
        numpy.savetxt(savename, (T, V, I, ti))  # save data to file
    
    s = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    s.login(email, password)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = 'subject'

    array = (T, V, I, ti)

    attachment = MIMEText(str(array), 'plain')
    attachment.add_header('Content-Disposition', 'attachment', filename='output.txt')
    msg.attach(attachment)
    with open(savename) as f:
        data = f.readlines()
    s.sendmail(email, emails, data)
    
    s.quit()


if __name__ == "__main__":
    args = get_args()

    # National Instruments GPIB-USB-HS GPIB interface
    Vdmm = K2000(16, 0)  # GPIB adaptor gpib0, device address 16
    Vdmm.write(":SENS:FUNC 'VOLT:DC'")  # configure to dc voltage
    Idmm = K2000(26, 0)  # GPIB adaptor gpib0, device address 26
    Idmm.write(":SENS:FUNC 'CURR:DC'")  # configure to dc current

    set_psu()

    wait_to_cool(args.temp)
    iterate_temp(args.npts, args.temp, args.tstep, args.savename, args.wait)

    PSU.OutputOff  # Turn off PSU output

    # Disconnect from instruments
    PSU.close()
    ITC.close()
    