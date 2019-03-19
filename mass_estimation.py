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

file_location = 'Post_Flight_Datasheet_07_03_V3.xlsx'
workbook = xlrd.open_workbook(file_location)
sheet2 = workbook.sheet_by_index(0)

BEM_cg = 7.421372 #[m]

Fmass = []      #Fuel mass in [kg]
Fmoment = []    #Fuel moment in [kg*m]
Pmass = []        #Pax mass in [kg]
Pmoment = []    #Pax moment in [kg*m]

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
    Pmoment.append((sheet1.cell_value(i,4)*Pmass[i-1][0]*(InchToM*LbsToKg)*9.81))
Pmoment = np.array(Pmoment).reshape(-1,1)


#Use Regression model from sklearn to get fuel moment function
lm = linear_model.LinearRegression()
lm.fit(Fmass,Fmoment)

#Define coefficient of fuel moment function
a = (lm.coef_)[0][0]
b = (lm.predict(np.array([0]).reshape(-1,1)))[0][0]



