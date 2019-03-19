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

Weight = Constants['Basicemptyweight'] + np.sum(Payload) + Constants['Fuelref'] - Fburned #kg

#Calculating Cn using the Cl-Cd data from stat1
#Cn = Cl * cos(AoA) +Cd * sin(AoA)
Cn = (Stat1Results['ClAlphaCoef'][0]*AoA+Stat1Results['ClAlphaCoef'][1])*np.cos(AoArad) \
    + (Stat1Results['CdAlphaCoef'][0]*AoA**2+ \
       Stat1Results['CdAlphaCoef'][1]*AoA+Stat1Results['CdAlphaCoef'][2]) * np.sin(AoArad)
    
xcg = np.array(([CG_pre],[CG_post])) #m
Cmdeltaconstant = ((xcg[1]-xcg[0])/Constants['Chord']) * -(1/(eldefrad[-1]-eldefrad[-2]))
Cmdelta = Cmdeltaconstant * Cn[-1]

#Thrust 
ThrustrefL = np.array(([1912.71],[1955.14],[1990.61],[2024.82],[2024.82],[1876.69],[1862.96])) #N
ThrustrefR = np.array(([2087.71],[2132.88],[2161.77],[2208.58],[2048.16],[2050.41],[2023.09])) #N
Thrustref = ThrustrefL+ThrustrefR #N

#IAS to TAS and actual density calculation
rhoact = Constants['rho_0ISA'] * ((T/Constants['T_0ref'])**(-(Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA'])+1))) #kg/m^3

Vcal = IAS2-(2*0.514444) #m/s
VTAS = eq_speed(h,T,Constants,Vcal) * np.sqrt(Constants['rho_0ISA']/rhoact) #m/s
VTAS = VTAS.reshape(-1,1) #m/s


#Thrustcoefficient Tc using total thrust
Tc = (Thrustref)/(0.5*rhoact[0:7]*(VTAS[0:7]**2)*Constants['Dengine']**2) #N, using thrust of 1 engine, avarage between the 2

#Thrustcoefficient Tcs using total standard thrust
Tps1engine = np.array(([1335.52],[1395.28],[1448.37],[1511.91],[1289.79],[1250.56],[1181.27])) #N
Tps = Tps1engine*2 #N
Tcs = (Tps)/(0.5*rhoact[0:7]*(VTAS[0:7]**2)*Constants['Dengine']**2) 

#deltaeq*
eldefstarrad = eldefrad[0:7] - ((1/Cmdelta)*Constants['CmTc']*(Tcs-Tc)) #radian
eldefstar = np.degrees(eldefstarrad) #degrees

#Festar
Festar = Fe[0:7]*(Constants['Ws']/(Weight[0:7]*Constants['g_0']))

#Vetilde
Vetilde = eq_speed(h,T,Constants,Vcal)[0:7]*np.sqrt(Constants['Ws']/(Weight[0:7]*Constants['g_0'])) 

Vcal = IAS2-(2*0.514444) #m/s
VTAS = eq_speed(h,T,Constants,Vcal) * np.sqrt(Constants['rho_0ISA']/rhoact) #m/s
VTAS = VTAS.reshape(-1,1) #m/s


#linear regression trim curve
lm = linear_model.LinearRegression()
lm.fit(Vetilde,eldefstar)

#Thrustcoefficient Tc using total thrust
Tc = (Thrustref)/(0.5*rhoact[0:7]*(VTAS[0:7]**2)*Constants['Dengine']**2) #N, using thrust of 1 engine, avarage between the 2

#Thrustcoefficient Tcs using total standard thrust
Tps1engine = np.array(([1335.52],[1395.28],[1448.37],[1511.91],[1289.79],[1250.56],[1181.27])) #N
Tps = Tps1engine*2 #N
Tcs = (Tps)/(0.5*rhoact[0:7]*(VTAS[0:7]**2)*Constants['Dengine']**2) 

#Festar
Festar = Fe[0:7]*(Constants['Ws']/(Weight[0:7]*Constants['g_0']))

#Vetilde
Vetilde = eq_speed(h,T,Constants,Vcal)[0:7]*np.sqrt(Constants['Ws']/(Weight[0:7]*Constants['g_0'])) 

#linear regression trim curve
lm = linear_model.LinearRegression()
lm.fit(Vetilde,eldefstar)

#polynomial regression for stick force
VetildePoly = []
for i in Vetilde:
    VetildePoly.append(float(i[0]))
           

FestarPoly = []
for i in Festar:
    FestarPoly.append(float(i[0]))

FestarRegressed = []
    
PolyCoef = np.polyfit(VetildePoly,FestarPoly,2)
Vetilde_range = np.arange(55,100,0.01)
for spd in Vetilde_range:
    FestarRegressed.append(((PolyCoef[0]*spd**2)+(PolyCoef[1]*spd)+PolyCoef[2]))
FestarRegressed = np.array(FestarRegressed).reshape(-1,1)


plt.figure('trim curve')
plt.plot(Vetilde,eldefstar,'ro')
plt.plot(Vetilde,lm.predict(Vetilde))
plt.gca().invert_yaxis()

plt.figure('Stick force curve')
plt.plot(Vetilde,Festar,'ro')

plt.plot(Vetilde_range,FestarRegressed)

plt.gca().invert_yaxis()









    
