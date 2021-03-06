import xlrd 
import numpy as np
import math
from Constantsdictonary import Constants
import matplotlib.pyplot as plt
from Stat1 import Stat1Results 
from appendix_b import eq_speed
from mass_estimation import CG_post,CG_pre
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

DataBook = Stat1Results["DataBook"]
ShowFigures = Stat1Results["ShowFigures"]

if DataBook == "R":
    file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
    excelrange = np.hstack((np.arange(58,65),np.arange(74,76)))
    excelrange2 = np.arange(58,65)
    
else:
    file_location = 'Post_Flight_Datasheet_07_03_V3.xlsx' #'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
    excelrange = np.hstack((np.arange(58,63),np.arange(74,76)))
    excelrange2 = np.arange(58,63)

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
ThrustrefL = [] #N
ThrustrefR = [] #N
Tps1engine = []

#7 measurements + cg shift measurements
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
for i in excelrange2:
    ThrustrefL.append(float(sheet.cell_value(i,13)))
ThrustrefL = np.array(ThrustrefL).reshape(-1,1)
for i in excelrange2:
    ThrustrefR.append(float(sheet.cell_value(i,14)))
ThrustrefR = np.array(ThrustrefR).reshape(-1,1)
for i in excelrange2:
    Tps1engine.append(float(sheet.cell_value(i,15)))
Tps1engine = np.array(Tps1engine).reshape(-1,1)
for i in np.arange(7,16):
    Payload.append(sheet.cell_value(i,7))
Payload = np.array(Payload).reshape(-1,1)

#Calculation sea level rotterdam
P0rot = Constants['p_0ISA'] *(Constants['T_0ref']/Constants['T_0ISA'])**(-Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))
rho0rot = Constants['rho_0ISA'] *(Constants['T_0ref']/Constants['T_0ISA'])**-((Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))+1)

#Cg shift 2 measurements 
Weight = Constants['Basicemptyweight'] + np.sum(Payload) + Constants['Fuelref'] - Fburned #kg

#Calculating Cn using the Cl-Cd data from stat1
#Cn = Cl * cos(AoA) +Cd * sin(AoA)
Cn = (Stat1Results['ClAlphaCoef'][0]*AoA+Stat1Results['ClAlphaCoef'][1])*np.cos(AoArad) \
    + (Stat1Results['CdAlphaCoef'][0]*AoA**2+ \
       Stat1Results['CdAlphaCoef'][1]*AoA+Stat1Results['CdAlphaCoef'][2]) * np.sin(AoArad)
    
xcg = np.vstack(([CG_pre],[CG_post])) #m
Cmdeltaconstant = ((xcg[1]-xcg[0])/Constants['Chord']) * -(1/(eldefrad[-1]-eldefrad[-2]))
Cmdelta = Cmdeltaconstant * Cn[-1]

#Thrust 
Thrustref = ThrustrefL+ThrustrefR #N

#calculating actual density
rhoact = rho0rot *(T/Constants['T_0ref'])**-((Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))+1) #kg/m^3

Vcal = IAS2-(2*0.514444) #m/s
VTAS,M,pact = eq_speed(h,T,Constants,Vcal,P0rot,rho0rot)


#Thrustcoefficient Tc using total thrust
Tc = (Thrustref)/(0.5*rhoact[0:len(Thrustref)]*(VTAS[0:len(Thrustref)]**2)*Constants['Dengine']**2) #N, using thrust of 1 engine, avarage between the 2

#Thrustcoefficient Tcs using total standard thrust
Tps = Tps1engine*2 #N
Tcs = (Tps)/(0.5*rhoact[0:len(Thrustref)]*(VTAS[0:len(Thrustref)]**2)*Constants['Dengine']**2) 

#deltaeq*
eldefstarrad = eldefrad[0:len(Thrustref)] - ((1/Cmdelta)*Constants['CmTc']*(Tcs-Tc)) #radian
eldefstar = np.degrees(eldefstarrad) #degrees

#polynomial regression for deltaeq*

#Festar
Festar = Fe[0:len(Thrustref)]*(Constants['Ws']/(Weight[0:len(Thrustref)]*Constants['g_0']))

#Vetilde
Vetilde = VTAS[0:len(Thrustref)]*np.sqrt(rhoact[0:len(Thrustref)]/rho0rot)*np.sqrt(Constants['Ws']/(Weight[0:len(Thrustref)]*Constants['g_0'])) 

#linear regression trim curve versus AoA 
lm = linear_model.LinearRegression()
lm.fit(AoArad[0:len(Thrustref)],eldefstarrad[0:len(Thrustref)])
eldefstarAoArad = lm.predict(AoArad[0:len(Thrustref)])

#Getting Cma from the elevator trim curve versus AoA
Cma = lm.coef_ * -Cmdelta

#polynomial regression for stick force
VetildePoly = []
for i in Vetilde:
    VetildePoly.append(float(i[0]))
           
FestarPoly = []
for i in Festar:
    FestarPoly.append(float(i[0]))

EldefPoly = []
for i in eldefstar:
    EldefPoly.append(float(i[0]))

FestarRegressed = []
eldefstarRegressed = []
    
PolyFestarCoef = np.polyfit(VetildePoly,FestarPoly,2)
PolyEldefCoef = np.polyfit(VetildePoly,EldefPoly,2)
Vetilde_range = np.arange(70,100,0.01)

for spd in Vetilde_range:
    FestarRegressed.append(((PolyFestarCoef[0]*spd**2)+(PolyFestarCoef[1]*spd)+PolyFestarCoef[2]))
    eldefstarRegressed.append(((PolyEldefCoef[0]*spd**2)+(PolyEldefCoef[1]*spd)+PolyEldefCoef[2]))
FestarRegressed = np.array(FestarRegressed).reshape(-1,1)


if ShowFigures == "Yes":
    
    plt.figure('trim curve - alpha')
    plt.title("Trim curve - "+ r'$\alpha$')
    plt.plot(AoA[0:len(Thrustref)],eldefstar,'ro', label='Measured data')
    plt.plot(AoA[0:len(Thrustref)],np.degrees(eldefstarAoArad), label='Linear regressed')
    plt.ylabel("eldefstar")
    plt.xlabel(r'$\alpha$[deg]')
    plt.gca().invert_yaxis()
    plt.legend()
    
    plt.figure('trim curve')
    plt.title('Trim curve')
    plt.plot(Vetilde,eldefstar,'ro', label='Measured data')
    plt.plot(Vetilde_range,eldefstarRegressed, label='Polynomial regressed')
    plt.ylabel("eldefstar")
    plt.xlabel('$V\~e$ [m/s]')
    plt.gca().invert_yaxis()
    plt.legend()


    plt.figure('Stick force curve')
    plt.title('Stick force curve')
    plt.plot(Vetilde,Festar,'ro', label='Measured data')
    plt.plot(Vetilde_range,FestarRegressed, label='Polynomial regressed')
    plt.ylabel("Force [N]")
    plt.xlabel('$V\~e$ [m/s]')
    plt.gca().invert_yaxis()
    plt.legend()










    
