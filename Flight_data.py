import flightdata_reader
import xlrd 
from Stat1 import Stat1Results 
import numpy as np

#Conversion 
Feetmeter = 0.3048
Knotsmeter = 0.514444
Poundkg = 0.45359237
Degtorad = (np.pi/180)
Radtodeg = (180/np.pi)

#Importing flight data ________________________________________________________
flightdata = flightdata_reader.flightdata

#Importing excel data _________________________________________________________

DataBook = Stat1Results["DataBook"]

if DataBook == "R":
    file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
    
else:
    file_location = 'Post_Flight_Datasheet_07_03_V3.xlsx'
    
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)


#Definition that changes the time from the format 1:01:23 into seconds
def timechange(t):
    
    tc = t*24*3600
#    if len(t) == 4:
#        tc = int(t[0:1])*60 + int(t[2:4])
#    if len(t) == 5:
#        tc = int(t[0:2])*60 + int(t[3:5])
#    if len(t) == 7:
#        tc = int(t[0])*3600 + int(t[2:4])*60 + int(t[5:7])
    return tc
    
#Starting times of eigenmotions
st_ph  = int(timechange(sheet.cell_value(82,3))) #starting time phugoid
st_shp = int(timechange(sheet.cell_value(83,3))) #starting time short period
st_dr  = int(timechange(sheet.cell_value(82,6))) #starting time dutch roll
st_drd = int(timechange(sheet.cell_value(83,6))) #starting time dutch roll damp
st_ar  = int(timechange(sheet.cell_value(82,9))) #starting time aperiodic roll 
st_spi = int(timechange(sheet.cell_value(83,9))) #starting time spiral

#time corrections of eigenmotions, these times are added to the starting time
correction_ph = 30
correction_shp = 11
correction_dr = 10
correction_drd = 10
correction_ar = 44
correction_spi = 20

#Durations of the eigenmotions
duration_ph = 175 
duration_shp = 10 
duration_dr = 25 #12 is best time span but let it 25 to show statespace exploding somehow
duration_drd = 12 #12 is best time span but let it 25 to show statespace exploding somehow
duration_ar =16 
duration_spi = 310 

#______________________________________________________________________________        <------
#------------------------------------------------------------------------------        <------
#                                SITUATION
#------------------------------------------------------------------------------        <------
#______________________________________________________________________________        <------
situation = 3 #Phugoid (0),Short period (1),Dutch roll (2),Dutch roll damp(3)
              #Aperiodic roll (4), Spiral (5)
              
#______________________________________________________________________________        <------
#------------------------------------------------------------------------------        <------
#______________________________________________________________________________        <------
              
              
st = [st_ph,st_shp,st_dr,st_drd,st_ar,st_spi] #starting times eigenmotions
cor = [correction_ph,correction_shp,correction_dr,correction_drd,correction_ar,correction_spi]
dur = [duration_ph,duration_shp,duration_dr,duration_drd,duration_ar,duration_spi]

st_interval = ((st[situation]-9+cor[situation])*10)
end_interval = ((st[situation]-9+cor[situation]+dur[situation])*10+1)

#Importing variables 
time = flightdata['flightdata']['time']['data']

Vtrue = flightdata['flightdata']['Dadc1_tas']['data']*Knotsmeter
AoA = flightdata['flightdata']['vane_AOA']['data']*Degtorad
pitchA = flightdata['flightdata']['Ahrs1_Pitch']['data']*Degtorad
press_alt = flightdata['flightdata']['Dadc1_alt']['data']*Feetmeter

F_used_L = flightdata['flightdata']['lh_engine_FU']['data']*Poundkg
F_used_R = flightdata['flightdata']['rh_engine_FU']['data']*Poundkg

pitchrate = flightdata['flightdata']['Ahrs1_bPitchRate']['data']*Degtorad
yawrate = flightdata['flightdata']['Ahrs1_bYawRate']['data']*Degtorad
rollrate = flightdata['flightdata']['Ahrs1_bRollRate']['data']*Degtorad
rollA = flightdata['flightdata']['Ahrs1_Roll']['data']*Degtorad

truehead = flightdata['flightdata']['Fms1_trueHeading']['data']

eldefflight = flightdata['flightdata']['delta_e']['data']*Degtorad
adefflight = flightdata['flightdata']['delta_a']['data']*Degtorad
rdefflight = flightdata['flightdata']['delta_r']['data']*Degtorad
