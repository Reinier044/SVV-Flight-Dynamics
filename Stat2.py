import xlrd 
import numpy as np
import math
from Constantsdictonary import Constants
import matplotlib.pyplot as plt
from Stat1 import Stat1Results

file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

#-------------------------Second stationary Measurements--------------------#
h = []
IAS = []
AoA = []
AoArad = []
eldef = []
eldefrad = []
trimdef = []
Fe = []
Fburned = []
T = [] 
Payload = []

#7 measurements + cg shift measurements
excelrange = np.hstack((np.arange(58,65),np.arange(74,76)))

for i in excelrange:
    h.append((sheet.cell_value(i,3)*0.3048))
h = np.array(h).reshape(-1,1)
for i in excelrange:
    IAS.append((sheet.cell_value(i,4)*0.514444))
IAS2 = np.array(IAS).reshape(-1,1)
for i in excelrange:
    AoA.append((float(sheet.cell_value(i,5))))
AoA = np.array(AoA).reshape(-1,1)
for i in range(len(AoA)):   
    AoArad.append(math.radians(AoA[i]))
AoArad = np.array(AoArad).reshape(-1,1)
for i in excelrange:
    eldef.append((float(sheet.cell_value(i,6))))
eldef = np.array(eldef).reshape(-1,1)
for i in range(len(AoA)):   
    eldefrad.append(math.radians(eldef[i]))
eldefrad = np.array(eldefrad).reshape(-1,1)
for i in excelrange:
    trimdef.append(float(sheet.cell_value(i,7)))
trimdef = np.array(trimdef).reshape(-1,1)
for i in excelrange:
    Fe.append(sheet.cell_value(i,8))
Fe = np.array(Fe).reshape(-1,1)
for i in excelrange:
    Fburned.append(sheet.cell_value(i,11)*0.453592)
Fburned = np.array(Fburned).reshape(-1,1)
for i in excelrange:
    T.append(float(sheet.cell_value(i,12))+273.15)
T = np.array(T).reshape(-1,1)
for i in np.arange(7,16):
    Payload.append(sheet.cell_value(i,7))
Payload = np.array(Payload).reshape(-1,1)

#Cg shift 2 measurements 

Weight = Constants['Basicemptyweight'] + np.sum(Payload) + Constants['Fuelref'] - Fburned

#Calculating Cn using the Cl-Cd data from stat1
#Cn = Cl * cos(AoA) +Cd * sin(AoA)
Cn = (Stat1Results['ClAlphaCoef'][0]*AoA+Stat1Results['ClAlphaCoef'][1])*np.cos(AoArad) \
    + (Stat1Results['CdAlphaCoef'][0]*AoA**2+ \
       Stat1Results['CdAlphaCoef'][1]*AoA+Stat1Results['CdAlphaCoef'][2]) * np.sin(AoArad)
    
xcg = np.array(([7.149610014],[7.115209049]))
Cmdeltaconstant = ((xcg[1]-xcg[0])/Constants['Chord']) * -(1/(eldefrad[-1]-eldefrad[-2]))
Cmdelta = Cmdeltaconstant * Cn[-1]













    
