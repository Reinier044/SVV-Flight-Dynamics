import flightdata_reader
import xlrd 
import numpy as np
import matplotlib.pyplot as plt
from Flight_data import *

#______________________________________________________________________________
#_________________________Creating lines to be plotted_________________________
#______________________________________________________________________________

#Lines to be plotted for phugoid ----------------------------------------------
correction_ph = 30 #correction used to start the plot at acual start of motion
duration_ph = 200 + correction_ph #duration of eigenmotion
t_int_ph_st = ((st_ph-9+correction_ph)*10)  #timeframe starting point
t_int_ph_end = ((st_ph-9+duration_ph)*10+1) #timeframe ending point

#Changing the needed arrays to arrays of the eigenmotion itself
t_ph = time[t_int_ph_st:t_int_ph_end]
AoA_ph = AoA[t_int_ph_st:t_int_ph_end]
pitch_ph = pitchA[t_int_ph_st:t_int_ph_end]
pitchrate_ph = pitchrate[t_int_ph_st:t_int_ph_end]
Vtrue_ph = Vtrue[t_int_ph_st:t_int_ph_end]

#Lines to be plotted for short-period -----------------------------------------
correction_shp = 11 #correction used to start the plot at acual start of motion
duration_shp = 8 + correction_shp #duration of eigenmotion
t_int_shp_st = ((st_shp-9+correction_shp)*10)  #timeframe starting point
t_int_shp_end = ((st_shp-9+duration_shp)*10+1) #timeframe ending point

#Changing the needed arrays to arrays of the eigenmotion itself
t_shp = time[t_int_shp_st:t_int_shp_end] 
AoA_shp = AoA[t_int_shp_st:t_int_shp_end]
pitch_shp = pitchA[t_int_shp_st:t_int_shp_end]
pitchrate_shp = pitchrate[t_int_shp_st:t_int_shp_end]
Vtrue_shp = Vtrue[t_int_shp_st:t_int_shp_end]

#lines to be plotted for dutch roll undamped ----------------------------------
correction_dr = 10 #correction used to start the plot at acual start of motion
duration_dr = 30 + correction_dr #duration of eigenmotion
t_int_dr_st = ((st_dr-9+correction_dr)*10)  #timeframe starting point
t_int_dr_end = ((st_dr-9+duration_dr)*10+1) #timeframe ending point

#Changing the needed arrays to arrays of the eigenmotion itself
t_dr = time[t_int_dr_st:t_int_dr_end]
AoA_dr = AoA[t_int_dr_st:t_int_dr_end]
pitch_dr = pitchA[t_int_dr_st:t_int_dr_end]
pitchrate_dr = pitchrate[t_int_dr_st:t_int_dr_end]
rollrate_dr = rollrate[t_int_dr_st:t_int_dr_end]
rollA_dr = rollA[t_int_dr_st:t_int_dr_end]

#lines to be plotted for dutch roll damped ----------------------------------
correction_drd = 10 #correction used to start the plot at acual start of motion
duration_drd = 25 + correction_drd #duration of eigenmotion
t_int_drd_st = ((st_drd-9+correction_drd)*10)  #timeframe starting point
t_int_drd_end = ((st_drd-9+duration_drd)*10+1) #timeframe ending point

#Changing the needed arrays to arrays of the eigenmotion itself
t_drd = time[t_int_drd_st:t_int_drd_end]
AoA_drd = AoA[t_int_drd_st:t_int_drd_end]
pitch_drd = pitchA[t_int_drd_st:t_int_drd_end]
pitchrate_drd = pitchrate[t_int_drd_st:t_int_drd_end]
rollrate_drd = rollrate[t_int_drd_st:t_int_drd_end]
rollA_drd = rollA[t_int_drd_st:t_int_drd_end]

#Lines to be plotted for Aperiodic role ---------------------------------------
correction_ar = 40 #correction used to start the plot at acual start of motion
duration_ar =30 + correction_ar #duration of eigenmotion
t_int_ar_st = ((st_ar-9+correction_ar)*10)  #timeframe starting point
t_int_ar_end = ((st_ar-9+duration_ar)*10+1) #timeframe ending point

#Changing the needed arrays to arrays of the eigenmotion itself
t_ar = time[t_int_ar_st:t_int_ar_end]
AoA_ar = AoA[t_int_ar_st:t_int_ar_end]
pitch_ar = pitchA[t_int_ar_st:t_int_ar_end]
pitchrate_ar = pitchrate[t_int_ar_st:t_int_ar_end]
rollrate_ar = rollrate[t_int_ar_st:t_int_ar_end]
rollA_ar = rollA[t_int_ar_st:t_int_ar_end]

#Lines to be plotted for Spiral -----------------------------------------------
correction_spi = 20 #correction used to start the plot at acual start of motion
duration_spi = 310 + correction_spi #duration of eigenmotion
t_int_spi_st = ((st_spi-9+correction_spi)*10)  #timeframe starting point
t_int_spi_end = ((st_spi-9+duration_spi)*10+1) #timeframe ending point

#Changing the needed arrays to arrays of the eigenmotion itself
t_spi = time[t_int_spi_st:t_int_spi_end]
AoA_spi = AoA[t_int_spi_st:t_int_spi_end]
pitch_spi = pitchA[t_int_spi_st:t_int_spi_end]
pitchrate_spi = pitchrate[t_int_spi_st:t_int_spi_end]
rollrate_spi = rollrate[t_int_spi_st:t_int_spi_end]
rollA_spi = rollA[t_int_spi_st:t_int_spi_end]

#______________________________________________________________________________
#____________________________________PLOTS_____________________________________
#______________________________________________________________________________


#------------------------------------------------------------------------------
##-------------------------------Plots Phugoid---------------------------------
#------------------------------------------------------------------------------
#The angle of attack, pitch angle and rate and the true airspeed can be plotted


#plt.plot(t_ph,AoA_ph,label="AoA")
#plt.plot(t_ph,pitch_ph,label="Pitch angle")
#plt.plot(t_ph,pitchrate_ph,label='Pitch Rate')
##plt.plot(t_ph,Vtrue_ph,label="True Airspeed")
#
#plt.axvline(x=(st_ph+correction_ph),color='r')
#plt.axhline(y=0,color='g')
#
#plt.title("Phugoid")
#plt.legend()
#
#plt.show


#------------------------------------------------------------------------------
##------------------------------Plots Short period-----------------------------
#------------------------------------------------------------------------------
#The angle of attack, pitch angle and rate and the true airspeed can be plotted


#plt.plot(t_shp,AoA_shp,label="AoA")
#plt.plot(t_shp,pitch_shp,label="Pitch angle")
#plt.plot(t_shp,pitchrate_shp,label='Pitch Rate')
##plt.plot(t_shp,Vtrue_shp,label="True Airspeed")
#
#plt.axvline(x=(st_shp+correction_shp),color='r')
#plt.axhline(y=0,color='g')
#
#plt.title("Short-Period")
#plt.legend()
#
#plt.show


#------------------------------------------------------------------------------
#-----------------------------Plots Dutch role undamped -----------------------
#------------------------------------------------------------------------------

#plt.plot(t_dr,AoA_dr,label="AoA")
#plt.plot(t_dr,pitch_dr,label="Pitch angle")
#plt.plot(t_dr,pitchrate_dr,label='Pitch Rate')
#plt.plot(t_dr,rollrate_dr,label='Roll Rate')
#plt.plot(t_dr,rollA_dr,label='Roll angle')
#
#plt.axvline(x=(st_dr+correction_dr),color='r')
#plt.axhline(y=0,color='g')
#
#plt.title("Dutch Role undamped")
#plt.legend()
#
#plt.show


#------------------------------------------------------------------------------
#------------------------------Plots Dutch role undamped ----------------------
#------------------------------------------------------------------------------

#plt.plot(t_drd,AoA_drd,label="AoA")
#plt.plot(t_drd,pitch_drd,label="Pitch angle")
#plt.plot(t_drd,pitchrate_drd,label='Pitch Rate')
#plt.plot(t_drd,rollrate_drd,label='Roll Rate')
#plt.plot(t_drd,rollA_drd,label='Roll angle')
#
#plt.axvline(x=(st_drd+correction_drd),color='r')
#plt.axhline(y=0,color='g')
#
#plt.title("Dutch Role damped")
#plt.legend()
#
#plt.show


#------------------------------------------------------------------------------
#------------------------------Plots Aperiodic role----------------------------
#------------------------------------------------------------------------------

plt.plot(t_ar,AoA_ar,label="AoA")
plt.plot(t_ar,pitch_ar,label="Pitch angle")
plt.plot(t_ar,pitchrate_ar,label='Pitch Rate')
plt.plot(t_ar,rollrate_ar,label='Roll Rate')
plt.plot(t_ar,rollA_ar,label='Roll angle')

plt.axvline(x=(st_ar+correction_ar),color='r')
plt.axhline(y=0,color='g')

plt.title("Aperiodic Role")
plt.legend()

plt.show


#------------------------------------------------------------------------------
#------------------------------Plots Spiral------------------------------------
#------------------------------------------------------------------------------

#plt.plot(t_spi,AoA_spi,label="AoA")
#plt.plot(t_spi,pitch_spi,label="Pitch angle")
#plt.plot(t_spi,pitchrate_spi,label='Pitch Rate')
#plt.plot(t_spi,rollrate_spi,label='Roll Rate')
#plt.plot(t_spi,rollA_spi,label='Roll angle')
#
#plt.axvline(x=(st_spi+correction_spi),color='r')
#plt.axhline(y=0,color='g')
#
#plt.title("Spiral")
#plt.legend()
#
#plt.show






















#starteig = 300
#timeeig = time[((st_ph-9-starteig)*10):-1]
#rollAeig = rollA[((st_ph-9-starteig)*10):-1]
#AoAeig = AoA[((st_ph-9-starteig)*10):-1]
#pitchAeig = pitchA[((st_ph-9-starteig)*10):-1]
#pitchrateeig = pitchrate[((st_ph-9-starteig)*10):-1]
#rollrateeig = rollrate[((st_ph-9-starteig)*10):-1]
#yawrateeig = yawrate[((st_ph-9-starteig)*10):-1]
#
##Plots of everything
#plt.plot(timeeig,rollAeig, label="Roll")
#plt.plot(timeeig,AoAeig, label="AoA")
#plt.plot(timeeig,pitchAeig, label="PitchA")
#plt.plot(timeeig,pitchrateeig, label="pitchrate")
##plt.plot(timeeig,rollrateeig, label="rollrate")
##plt.plot(timeeig,yawrateeig, label="yawrate")
#plt.axvline(x=st_ph,color='r')
#plt.legend()
#plt.show