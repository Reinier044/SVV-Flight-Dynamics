import numpy as np
from Cit_par import *
import control.matlab as ml
import control as ctr
import matplotlib.pyplot as plt
from Flight_data import *
from Validation import *
from Constantsdictonary import Constants
#Symmetric Flight ____________________________________________________________
Dc = Constants['Chord']/V0

Pdot = np.array([[-2*muc*Dc*(1/V0),0,0,0],\
                 [0,(CZadot-2*muc)*Dc,0,0],\
                 [0,0,-Dc,0],\
                 [0,Cmadot*Dc,0,-2*muc*KY2*Dc*(Constants['Chord']/V0)]])

Q = np.array([[-CXu/V0,-CXa,-CZ0,-CXq*(Constants['Chord']/V0)],\
              [-CZu/V0,-CZa,CX0,(-CZq-2*muc)*(Constants['Chord']/V0)],\
              [0,0,0,-1*(Constants['Chord']/V0)],\
              [-Cmu/V0,-Cma,0,-Cmq*(Constants['Chord']/V0)]])

R = np.array([[-CXde],\
              [-CZde],\
              [0],\
              [-Cmde]])

A_s = np.dot(np.linalg.inv(Pdot),Q)

B_s = np.dot(np.linalg.inv(Pdot),R)

C_s = np.identity(4)

D_s = np.zeros((4,1))

Sys_s = ml.ss(A_s,B_s,C_s,D_s)

duration_shp = 50
u = (eldefflight[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]*(np.pi/180))-(eldefflight[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)][0]*(np.pi/180))
t = time[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]

sol = ml.lsim(Sys_s,U=u,T=t)
#sol = ctr.forced_response(Sys_s,U=u,T=t)


plt.figure('response')
plt.plot(sol[1],(sol[0][:,2]*(180/np.pi)))
plt.plot(sol[1],pitchA[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)])
plt.show

eigval_s,eigvec_s = np.linalg.eig(A_s)