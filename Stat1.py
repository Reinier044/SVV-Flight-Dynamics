import xlrd 
import numpy as np
from appendix_b import eq_speed,Vcalibrated
import math
from Constantsdictonary import Constants
import matplotlib.pyplot as plt

file_location = 'C:/Users/maxke/Dropbox/Lucht en Ruimtevaart/Third Year Courses/Simulation, Verification and Validation/Ref data/REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)


h1 = [] #[m]
IAS1 = [] #[m/s]
AoA1 = [] #[deg]
T1 = [] #[K]
Fused = [] #[kg]
Payload = [] #[kg]

#importing the PFD from the excel sheet for the first stationary meas.
for i in np.arange(27,33):
    h1.append((sheet.cell_value(i,3)*0.3048))
for i in np.arange(27,33):
    IAS1.append((sheet.cell_value(i,4)*0.514444))
for i in np.arange(27,33):
    AoA1.append((sheet.cell_value(i,5)))
for i in np.arange(27,33):
    T1.append((float(sheet.cell_value(i,9))+273.15))
for i in np.arange(27,33):
    Fused.append((sheet.cell_value(i,8))*0.453592)
for i in np.arange(7,16):
    Payload.append(sheet.cell_value(i,7))
    

#calculation of the density at the measurement points
rho1 = []
for i in np.arange(len(T1)):
    rhoact = Constants['rho_0ISA'] * ((T1[i]/Constants['T_0ISA'])**(-(Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA'])+1)))
    rho1.append(rhoact)

#Cl and CD calculation
Cl = []
Cl1 = []

Vcal1 = []
for i in range(len(IAS1)):
    Vcal1.append(Vcalibrated(Constants,IAS1[i],T1[i],rho1[i]))

Vtas1 = []
for i in range(len(rho1)):
    rho = rho1[i]
    Vtas =  eq_speed(h1[i],T1[i],Constants,Vcal1[i]) * math.sqrt(Constants['rho_0ISA']/rho)
    Vtas1.append(Vtas)

Weight = []
for i in range(len(Fused)):
    Weight.append(Constants['Basicemptyweight']+np.sum(Payload)+Constants['Fuelref']-Fused[i])

for i in range(len(Vtas1)):
    Cl.append((Weight[i]*Constants['g_0'])/(0.5*rho1[i]*Constants['S']*Vtas1[i]**2))
    Cl1.append((Weight[i]*Constants['g_0'])/(0.5*Constants['rho_0ISA']*Constants['S']*Vcal1[i]**2))  #used calibrated now  
    
#Cd0
    
#oswald 
    
plt.figure()
plt.plot(AoA1,Cl)    
plt.plot(AoA1,Cl1) 