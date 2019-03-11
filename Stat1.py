import xlrd 
import numpy as np

#constants
rho0 = 1.225
T0 = 288.15
g = 9.81
R = 287
alayer = -0.0065


file_location = 'C:/Users/stijn/Documents/Aerospace Engineering/3rd Year/SVV/REFERENCE_Post_Flight_Datasheet_Flight.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet = workbook.sheet_by_index(0)

h1 = [] #[m]
IAS1 = [] #[m/s]
AoA1 = [] #[deg]
T1 = [] #[K]

for i in np.arange(27,33):
    h1.append((sheet.cell_value(i,3)*0.3048))
for i in np.arange(27,33):
    IAS1.append((sheet.cell_value(i,4)*0.514444))
for i in np.arange(27,33):
    AoA1.append((sheet.cell_value(i,5)))
for i in np.arange(27,33):
    T1.append((float(sheet.cell_value(i,9))+273.15))

rho1 = []
for i in np.arange(len(T1)):
    rho   = rho0 * ((T1[i]/T0)**(-(g/(R*alayer)+1)))
    rho1.append(rho)

#Cl and CD calculation
    
#Cd0
    
#oswald 