import xlrd 
import numpy as np
from appendix_b import eq_speed
import math
from Constantsdictonary import Constants
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.preprocessing import PolynomialFeatures

InchToM = 0.0254            #Inches to meters
LbsToKg = 0.453592          #Pounds to kg
MtoN = 0.000115212          #Moment to normal
C = Constants['Chord']      #chord at MAC

file_location = 'loading.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet1 = workbook.sheet_by_index(0)

file_location = 'REFERENCE_Post_Flight_Datasheet_Flight.xlsx' #'REFERENCE_Post_Flight_Datasheet_Flight.xlsx' 'Post_Flight_Datasheet_07_03_V3.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet2 = workbook.sheet_by_index(0)

BEM_cg = 7.421372 #[m]
BEM = 4157.17068 #[kg]
Fstart = (4050*LbsToKg) #Fuel at beginning of flight[kg]

Fmass = []      #Fuel mass in [kg]
Fmoment = []    #Fuel moment in [kg*m]
Pmass = []        #Pax mass in [kg]
Pmoment_pre = []    #Pax moment before cg shift in [kg*m]
Pmoment_post = []    #Pax moment after cg shift in [kg*m]

F_used_pre = float(sheet2.cell_value(74,11))*LbsToKg    #fuel used before cg shift[kg]
F_used_post = float(sheet2.cell_value(75,11))*LbsToKg   #fuel used after cg shift[kg]
F_actual_pre = Fstart-F_used_pre #Actual fuel in tank before cg shift[kg]
F_actual_post = Fstart-F_used_post #Actual fuel in tank after cg shift[kg]


for i in np.arange(1,51):
    Fmass.append(sheet1.cell_value(i,0)*LbsToKg)
Fmass = np.array(Fmass).reshape(-1,1)

for i in np.arange(1,51):
    Fmoment.append((sheet1.cell_value(i,1))*(InchToM*LbsToKg))
Fmoment = np.array(Fmoment).reshape(-1,1)

for i in np.arange(7,16):
    Pmass.append((sheet2.cell_value(i,7)))
Pmass.append(0)
Pmass = np.array(Pmass).reshape(-1,1)

for i in np.arange(1,11):
    Pmoment_pre.append((sheet1.cell_value(i,4)*Pmass[i-1][0]))
Pmoment_pre = np.array(Pmoment_pre).reshape(-1,1)

for i in np.arange(1,11):
    Pmoment_post.append((sheet1.cell_value(i,8)*Pmass[i-1][0]))
Pmoment_post = np.array(Pmoment_post).reshape(-1,1)

#-------------------Linear regression for fuel moment-----------------------
#Use Regression model from sklearn to get fuel moment function
lm = linear_model.LinearRegression()
lm.fit(Fmass,Fmoment)

#Define coefficient of fuel moment function
a = (lm.coef_)[0][0]
b = (lm.predict(np.array([0]).reshape(-1,1)))[0][0]
#--------------------------------------------------------------------------

Fuel_moment_pre = ((F_actual_pre*a) + b)      #Moment of fuel before cg shift
Fuel_moment_post = ((F_actual_post*a) + b)    #Moment of fuel after cg shift

TotalMoment_pre = sum(Pmoment_pre)+Fuel_moment_pre+(BEM*BEM_cg)      #total moment before cg shift [kg*m]
TotalWeight_pre = sum(Pmass)+F_actual_pre+BEM                  #total mass before cg shift [kg]
CG_pre = TotalMoment_pre/(TotalWeight_pre)             #CG position before cg shift [m]

TotalMoment_post = sum(Pmoment_post)+Fuel_moment_post+(BEM*BEM_cg)
TotalWeight_post = sum(Pmass)+F_actual_post+BEM
CG_post = TotalMoment_post/(TotalWeight_post)  