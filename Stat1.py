import xlrd 
import numpy as np
from appendix_b import eq_speed
import math
from Constantsdictonary import Constants
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

ShowFigures = 'No'

DataBook = input("Reference data or Flight data? type (R/F): ")

if DataBook == "R":
    file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
    excelrange = np.hstack(np.arange(27,33))  
    
else:
    file_location = 'Post_Flight_Datasheet_07_03_V3.xlsx' #'REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
    excelrange = np.arange(27,33)


workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

Stat1Results = {}
Stat1Results["DataBook"] = DataBook 
Stat1Results["ShowFigures"] = ShowFigures

Thrust = [] #[N]
h1 = [] #[m]
IAS1 = [] #[m/s]
AoA1 = [] #[deg]
T1 = [] #[K]
Fused = [] #[kg]
Payload = [] #[kg]
TLeft = [] #[N]
TRight = [] #[N]

#importing the PFD from the excel sheet for the first stationary meas.
for i in excelrange:
    h1.append((sheet.cell_value(i,3)*0.3048))
for i in excelrange:
    IAS1.append((sheet.cell_value(i,4)*0.514444))
for i in excelrange:
    AoA1.append((float(sheet.cell_value(i,5))))
for i in excelrange:
    T1.append((float(sheet.cell_value(i,9))+273.15))
for i in excelrange:
    Fused.append((sheet.cell_value(i,8))*0.453592)
for i in excelrange:
    TLeft.append((sheet.cell_value(i,10)))
for i in excelrange:
    TRight.append((sheet.cell_value(i,11)))
for i in np.arange(7,16):
    Payload.append(sheet.cell_value(i,7))

    
#Calculate total thrust [N]
for i in range(len(TLeft)):
    Thrust.append(TLeft[i]+TRight[i])
    
#Calculation sea level rotterdam
P0rot = Constants['p_0ISA'] *(Constants['T_0ref']/Constants['T_0ISA'])**(-Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))
rho0rot = Constants['rho_0ISA'] *(Constants['T_0ref']/Constants['T_0ISA'])**-((Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))+1)

#calculation of Caibrated airspeed using table from the assignment
Vcal1 = []
for i in range(len(IAS1)):
    Vcal1.append(IAS1[i]-(2*0.514444))
    
#calculating true airspeed
Vtas1 = []
M1 = []
pact1 = []
for i in range(len(h1)):    
    Vtas,M,pact = eq_speed(h1[i],T1[i],Constants,Vcal1[i],P0rot,rho0rot)
    Vtas1.append(Vtas)
    M1.append(M)
    pact1.append(pact)
    
#calculating actual density
rho1 = []

for i in range(len(h1)):
    rhoact = rho0rot *(T1[i]/Constants['T_0ref'])**-((Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))+1)
    rho1.append(rhoact)
    
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

#Polynomial regression for Cl over Cd
CdPoly = []
for i in CdRev:
    CdPoly.append(float(i[0]))

ClPoly = []
for i in Cl:
    ClPoly.append(float(i[0]))

PolyCoefficients = np.polyfit(ClPoly,CdPoly,2)

ClTest = np.arange(0,1,0.01)

CdTest = []
for i in ClTest:
    CdTest.append(((i**2)*PolyCoefficients[0])+(i*PolyCoefficients[1])+(PolyCoefficients[2]))

#reynolds number range for the Cl-alpha curve
Reynolds = (np.array(rho1).reshape(-1,1)*np.array(Vtas1).reshape(-1,1)*Constants['MAC'])/Constants["dynamicviscosityair"]

#Use Regression model from sklearn for Cl over alpha and plotting the regression
AoA1 = np.array(AoA1).reshape(-1,1)
lm.fit(AoA1,Cl)
Clalpha = lm.coef_ *(180/np.pi)

#Add regression coefficients of Cl-alpha curve to the dictionary
a = (lm.coef_)[0][0]
b = (lm.predict(np.array([0]).reshape(-1,1)))[0][0]
Stat1Results["ClAlphaCoef"] = [a,b] #first one is a, second one is b with y = ax+ b
c = (((b**2)/(np.pi*Constants['A']*e))+Cd0)
b = ((2*a*b)/(np.pi*Constants['A']*e))
a = (((a**2)/(np.pi*Constants['A']*e)))
Stat1Results["CdAlphaCoef"] = [a,b,c] 
#,((2*(*(lm.coef_)[0][0])*((np.sqrt(lm.predict(np.array([0]).reshape(-1,1)))[0][0])))/(np.pi*Constants['A']*e)),((((lm.predict(np.array([0]).reshape(-1,1)))[0][0])/(np.pi*Constants['A']*e))+Cd0)]

AoA = np.arange(0,10,0.1).reshape(-1,1)

Cda = ((AoA**2)*a)+(AoA*b)+c


if ShowFigures == 'Yes':
    plt.figure('Cl-'+ r'$\alpha$')
    plt.plot(AoA,lm.predict(AoA), label = "Linear regression")
    plt.plot(AoA1,Cl, 'ro', label = "Measured data points")
    #plt.plot(AoA,Cda) 
    plt.ylabel("Cl [-]")
    plt.xlabel(r'$\alpha$' + "[degrees]")
    plt.title("Cl-"+ r'$\alpha$' + " for cruise configuration", loc = "left")
    plt.suptitle("Mach ["+str(round(float(M1[-1]),3))+" - "+str(round( \
                float(M1[0]),3))+"],"+"\n Reynolds ["+("{:.2e}".format( \
                Reynolds[-1][0]))+" - "+("{:.2e}".format(Reynolds[0][0]))+"]",\
                size='x-small', ha="left", y = '0.94')
    plt.legend()

    
    plt.figure('$C_L-C_D$')
    plt.title('$C_L-C_D$', loc = "left")
    plt.plot(CdTest,ClTest, color="blue",label='Polynomial regression') #Polynomial regression
    #plt.plot(CdRev,Cl, color="red") #Cd after linear regression
    plt.plot(Cd,Cl,'ro',color="red",label='Measured data') #Experimental data
    plt.suptitle("Mach ["+str(round(float(M1[-1]),3))+" - "+str(round( \
                float(M1[0]),3))+"],"+"\n Reynolds ["+("{:.2e}".format( \
                Reynolds[-1][0]))+" - "+("{:.2e}".format(Reynolds[0][0]))+"]",\
                size='x-small', ha="left", y = '0.94')
    plt.legend()

