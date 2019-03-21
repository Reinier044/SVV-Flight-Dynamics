import flightdata_reader
import xlrd 
import numpy as np
import matplotlib.pyplot as plt
from Flight_data import *

title = ['Phugoid','Short Period','Dutch Roll','Damped Dutch Roll','Aperiodic Roll','Spiral']

t = time[st_interval:end_interval]
AoA = AoA[st_interval:end_interval]
pitch = pitchA[st_interval:end_interval]
pitchrate = pitchrate[st_interval:end_interval]
rollrate = rollrate[st_interval:end_interval]
rollA = rollA[st_interval:end_interval]
Vtrue = Vtrue[st_interval:end_interval]

#plt.plot(t,AoA,label="AoA")
#plt.plot(t,pitch,label="Pitch angle")
#plt.plot(t,pitchrate,label='Pitch Rate')
#plt.plot(t,rollrate,label='Roll Rate')
#plt.plot(t,rollA,label='Roll angle')
#plt.title(title[situation])
#plt.legend()
#
#plt.show








