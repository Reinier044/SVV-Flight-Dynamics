import xlrd 
import numpy as np
from appendix_b import eq_speed
import math
from Constantsdictionary import Constants

file_location = 'C:/Users/maxke/Dropbox/Lucht en Ruimtevaart/Third Year Courses/Simulation, Verification and Validation/Ref data/REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)


h1 = [] #[m]
IAS1 = [] #[m/s]
AoA1 = [] #[deg]
T1 = [] #[K]

#importing the PFD from the excel sheet for the first stationary meas.
for i in np.arange(27,33):
    h1.append((sheet.cell_value(i,3)*0.3048))
for i in np.arange(27,33):
    IAS1.append((sheet.cell_value(i,4)*0.514444))
for i in np.arange(27,33):
    AoA1.append((sheet.cell_value(i,5)))
for i in np.arange(27,33):
    T1.append((float(sheet.cell_value(i,9))+273.15))

#calculation of the density at the measurement points
rho1 = []
for i in np.arange(len(T1)):
    rhoact = Constants['rho_0ISA'] * ((T1[i]/Constants['T_0ISA'])**(-(Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA'])+1)))
    rho1.append(rhoact)

#Cl and CD calculation
Cl = []
Vtas1 = []
for i in range(len(rho1)):
    rho = rho1[i]
    Vtas =  eq_speed(h1[i],T1[i],Constants,IAS1[i]) * math.sqrt(Constants['rho_0ISA']/rho)
    Vtas1.append(Vtas)
    
    
#Cd0
    
#oswald 