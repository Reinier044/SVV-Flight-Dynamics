import flightdata_reader
import xlrd 
import numpy as np
import matplotlib.pyplot as plt

#Importing flight data ________________________________________________________
flightdata = flightdata_reader.flightdata

#Importing excel data _________________________________________________________
file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

#Definition that changes the time from the format 1:01:23 into seconds
def timechange(t):
    if len(t) == 4:
        tc = int(t[0:1])*60 + int(t[2:4])
    if len(t) == 5:
        tc = int(t[0:2])*60 + int(t[3:5])
    if len(t) == 7:
        tc = int(t[0])*3600 + int(t[2:4])*60 + int(t[5:7])
    return tc
    
#Starting times of eigenmotions
st_ph  = timechange(sheet.cell_value(82,3)) #starting time phugoid
st_shp = timechange(sheet.cell_value(83,3)) #starting time short period
st_dr  = timechange(sheet.cell_value(82,6)) #starting time dutch roll
st_drd = timechange(sheet.cell_value(83,6)) #starting time dutch roll with damp
st_ar  = timechange(sheet.cell_value(82,9)) #starting time aperiodic roll 
st_spi = timechange(sheet.cell_value(83,9)) #starting time spiral

#Importing variables 
time = flightdata['flightdata']['time']['data']
AoA = flightdata['flightdata']['vane_AOA']['data']
pitchA = flightdata['flightdata']['Ahrs1_Pitch']['data']
pitchrate = flightdata['flightdata']['Ahrs1_bPitchRate']['data']
yawrate = flightdata['flightdata']['Ahrs1_bYawRate']['data']
rollrate = flightdata['flightdata']['Ahrs1_bRollRate']['data']
rollA = flightdata['flightdata']['Ahrs1_Roll']['data']
Vtrue = flightdata['flightdata']['Dadc1_tas']['data']


#Creating lines to be plotted__________________________________________________

#Lines to be plotted for phugoid
duration_ph = 300
t_ph = time[((st_ph-9)*10):((st_ph-9+duration_ph)*10+1)]
AoA_ph = AoA[((st_ph-9)*10):((st_ph-9+duration_ph)*10+1)]
pitch_ph = pitchA[((st_ph-9)*10):((st_ph-9+duration_ph)*10+1)]
pitchrate_ph = pitchrate[((st_ph-9)*10):((st_ph-9+duration_ph)*10+1)]

#Lines to be plotted for short-period
duration_shp = 5
t_shp = time[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]
AoA_shp = AoA[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]
pitch_shp = pitchA[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]
pitchrate_shp = pitchrate[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]


#Lines to be plotted for Aperiodic role
duration_ar = 5
t_ar = time[((st_ar-9)*10):((st_ar-9+duration_ar)*10+1)]
AoA_ar = AoA[((st_ar-9)*10):((st_ar-9+duration_ar)*10+1)]
pitch_ar = pitchA[((st_ar-9)*10):((st_ar-9+duration_ar)*10+1)]
pitchrate_ar = pitchrate[((st_ar-9)*10):((st_ar-9+duration_ar)*10+1)]
rollrate_ar = rollrate[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]
rollA_ar = rollA[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]
#PLOTS_________________________________________________________________________

##Plots Phugoid-------------------------------
#plt.plot(t_ph,AoA_ph,label="AoA")
#plt.title("Phugoid")
#plt.plot(t_ph,pitch_ph,label="Pitch angle")
#plt.plot(t_ph,pitchrate_ph,label='Pitch Rate')
#plt.axvline(x=st_ph,color='r')
#plt.axhline(y=0,color='g')
#plt.legend()
#plt.show

#Plots Short period---------------------------
plt.plot(t_shp,AoA_shp,label="AoA")
plt.title("Short-Period")
plt.plot(t_shp,pitch_shp,label="Pitch angle")
plt.plot(t_shp,pitchrate_shp,label='Pitch Rate')
plt.axvline(x=st_shp,color='r')
plt.axhline(y=0,color='g')
plt.legend()
plt.show

#Plots Aperiodic role-------------------------
plt.plot(t_shp,AoA_shp,label="AoA")
plt.title("Aperiodic Role")
plt.plot(t_shp,pitch_shp,label="Pitch angle")
plt.plot(t_shp,pitchrate_shp,label='Pitch Rate')
plt.axvline(x=st_shp,color='r')
plt.axhline(y=0,color='g')
plt.legend()
plt.show