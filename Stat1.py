import xlrd 
import numpy as np
from appendix_b import eq_speed
import math
from Constantsdictonary import Constants
import matplotlib.pyplot as plt
from sklearn import linear_model
import pandas as pd

file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)


    

Thrust = [] #[N]
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
    
#Thrust data of the first stationary measurements. Replace with actual values please
TLeft = [3698.85,3009.89,2401.16,1856.19,1882.01,2192.1]
TRight = [3803.04,3071.74,2527.55,2008.22,2062.5,2387.56]

for i in range(len(TLeft)):
    Thrust.append(TLeft[i]+TRight[i])
    

#calculation of the density at the measurement points
rho1 = []
for i in np.arange(len(T1)):
    rhoact = Constants['rho_0ISA'] * ((T1[i]/Constants['T_0ref'])**(-(Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA'])+1)))
    rho1.append(rhoact)

#calculation of Caibrated airspeed using table from the assignment
Vcal1 = []
for i in range(len(IAS1)):
    Vcal1.append(IAS1[i]-(2*0.514444))

#calculation of True airspeed using reduction of airspeed from assignment
Vtas1 = []
for i in range(len(rho1)):
    rho = rho1[i]
    Vtas =  eq_speed(h1[i],T1[i],Constants,Vcal1[i]) * math.sqrt(Constants['rho_0ISA']/rho)
    Vtas1.append(Vtas)

#Calculating the weight at each measurement point using used fuel
Weight = []
for i in range(len(Fused)):
    Weight.append(Constants['Basicemptyweight']+np.sum(Payload)+Constants['Fuelref']-Fused[i])

#Calculation of the lift coefficient using true airspeed and actual density
Cl = []
for i in range(len(Vtas1)):
    Cl.append((Weight[i]*Constants['g_0'])/(0.5*rho1[i]*Constants['S']*Vtas1[i]**2))
    
<<<<<<< HEAD

#Calculate Cd
Cd = []
for i in range(len(Thrust)):
    Cd.append(Thrust[i]/(0.5*rho1[i]*Constants['S']*Vtas1[i]**2))

#Squared values of Cl
Cl2 = []
for i in range(len(Thrust)):
    Cl2.append(Cl[i]**2)



#Regression
   
Cl2 = np.array(Cl2)
Cl2 = Cl2.reshape(-1,1)
print(Cl2)
Cd = np.array(Cd)
Cd = Cd.reshape(-1,1)

lm = linear_model.LinearRegression()
model = lm.fit(Cl2,Cd)

predictions = lm.predict(Cl2)
Slope = lm.coef_
#oswald 
  
#plots
plt.figure()
plt.plot(Cl2,predictions)
plt.plot(Cl2,Cd)    
=======
#Calculation of the drag coefficient using the true airspeed and actual density
Cd = []
for i in range(len(Thrust)):
    Cd.append(Thrust[i]/(0.5*rho1[i]*Constants['S']*Vtas1[i]**2))
    
#Cd0

    
#oswald 
  
#plots
plt.figure("CL")
plt.plot(AoA1,Cl)  
plt.figure("CD") 
plt.plot(AoA1,Cd) 
>>>>>>> 2d550b5300cf7e8f44bef16ca42546f4eb8ea256
