import flightdata_reader
import xlrd 


#Importing flight data ________________________________________________________
flightdata = flightdata_reader.flightdata

#Importing excel data _________________________________________________________
file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx' #'REFERENCE_Post_Flight_Datasheet_Flight.xlsx' 'Post_Flight_Datasheet_07_03_V3.xlsx'
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

#Importing variables 
time = flightdata['flightdata']['time']['data']

Vtrue = flightdata['flightdata']['Dadc1_tas']['data']
AoA = flightdata['flightdata']['vane_AOA']['data']
pitchA = flightdata['flightdata']['Ahrs1_Pitch']['data']
press_alt = flightdata['flightdata']['Dadc1_alt']['data']

F_used_L = flightdata['flightdata']['lh_engine_FU']['data']
F_used_R = flightdata['flightdata']['rh_engine_FU']['data']

pitchrate = flightdata['flightdata']['Ahrs1_bPitchRate']['data']
yawrate = flightdata['flightdata']['Ahrs1_bYawRate']['data']
rollrate = flightdata['flightdata']['Ahrs1_bRollRate']['data']
rollA = flightdata['flightdata']['Ahrs1_Roll']['data']

Vtrue = flightdata['flightdata']['Dadc1_tas']['data']
truehead = flightdata['flightdata']['Fms1_trueHeading']['data']
press_alt = flightdata['flightdata']['Dadc1_alt']['data']

eldefflight = flightdata['flightdata']['delta_e']['data']

