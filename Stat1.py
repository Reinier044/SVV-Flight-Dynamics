import xlrd 
import numpy as np
from appendix_b import eq_speed
import math
from Constantsdictonary import Constants
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

Stat1Results = {}

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
    AoA1.append((float(sheet.cell_value(i,5))))
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
Cl = np.array(Cl).reshape(-1,1)


#Calculate Cd
Cd = []

for i in range(len(Thrust)):
    Cd.append(Thrust[i]/(0.5*rho1[i]*Constants['S']*Vtas1[i]**2))
Cd = np.array(Cd).reshape(-1,1)

#Squared values of Cl
Cl2 = []
for i in range(len(Thrust)):
    Cl2.append(Cl[i]**2)
Cl2 = np.array(Cl2).reshape(-1,1)

#Use Regression model from sklearn for CL2 over Cd plot
lm = linear_model.LinearRegression()
lm.fit(Cl2,Cd)

#Define slope of regression for CL2 over Cd plot
Slope = lm.coef_

#oswald factor from Cl2 over Cd
e = float((1/Slope)/(np.pi*Constants['A']))

#Zero lift drag
Cd0 = float((lm.predict(Cl2) - (Cl2/(np.pi*Constants['A']*e)))[0])

#Redefine Cd as calculated with Cd0 and e
CdRev = Cd0 + (Cl2/(np.pi*Constants['A']*e))

#mach number range using Tactual and Vtas for the Cl-alpha curve
T1 = np.array(T1).reshape(-1,1)
Vtas1 = np.array(Vtas1).reshape(-1,1)

M1 = Vtas1/(np.sqrt(Constants["gammaair"] * Constants["Rgas"] * T1))


#Polynomial regression for Cl over Cd
CdPoly = []
for i in CdRev:
    CdPoly.append(float(i[0]))

ClPoly = []
for i in Cl:
    ClPoly.append(float(i[0]))

PolyCoefficients = np.polyfit(ClPoly,CdPoly,2)

ClTest = np.arange(0,0.81,0.01)

CdTest = []
for i in ClTest:
    CdTest.append(((i**2)*PolyCoefficients[0])+(i*PolyCoefficients[1])+(PolyCoefficients[2]))

#reynolds number range for the Cl-alpha curve
Reynolds = (np.array(rho1).reshape(-1,1)*Vtas1*Constants['MAC'])/Constants["dynamicviscosityair"]

#Use Regression model from sklearn for Cl over alpha and plotting the regression
AoA1 = np.array(AoA1).reshape(-1,1)
lm.fit(AoA1,Cl)

#Add regression coefficients of Cl-alpha curve to the dictionary
a = (lm.coef_)[0][0]
b = (lm.predict(np.array([0]).reshape(-1,1)))[0][0]
Stat1Results["ClAlphaCoef"] = [a,b] #first one is a, second one is b with y = ax+ b
c = (((b**2)/(np.pi*Constants['A']*e))+Cd0)
b = ((2*a*b)/(np.pi*Constants['A']*e))
a = (((a**2)/(np.pi*Constants['A']*e)))
Stat1Results["ClAlphaCoef"] = [a,b] #first one is a, second one is b with y = ax+ b
Stat1Results["CdAlphaCoef"] = [a,b,c] 
#,((2*(*(lm.coef_)[0][0])*((np.sqrt(lm.predict(np.array([0]).reshape(-1,1)))[0][0])))/(np.pi*Constants['A']*e)),((((lm.predict(np.array([0]).reshape(-1,1)))[0][0])/(np.pi*Constants['A']*e))+Cd0)]

AoA = np.arange(0,10,0.1).reshape(-1,1)

Cda = ((AoA**2)*a)+(AoA*b)+c


plt.figure('Cl-alpha')
plt.plot(AoA1,lm.predict(AoA1))
#plt.plot(AoA,Cda) 
plt.ylabel("Cl [-]")
plt.xlabel("alpha [degrees]")
plt.title("Cl-alpha for cruise configuration, \n Mach ["\
        +str(round(float(M1[-1]),3))+"-"+str(round(float(M1[0]),3))+"],"\
        +"\n Reynolds ["+str(float(Reynolds[-1]))+"-"+str(float(Reynolds[0]))+"]")
    
#Redefine Cd as calculated with Cd0 and e
CdRev = Cd0 + (Cl2/(np.pi*Constants['A']*e))

#plots
plt.figure("CL")
#plt.plot(AoA1,Cl)  
plt.figure("CD") 
plt.plot(ClTest,CdTest, color="blue") #Polynomial regression
plt.plot(Cl,CdRev, color="red") #Cd after linear regression
plt.plot(Cl,Cd, color="green") #Experimental data


