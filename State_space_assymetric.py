import numpy as np
from Cit_par import *
import control.matlab as ml
import matplotlib.pyplot as plt
import numpy as np
from Constantsdictonary import Constants
from Flight_data import *

Db = Constants['Span']/V0
dimcor = 0.5*Constants['Span']/V0

P_a = np.array([[((CYbdot-2*mub)*Db),0,0,0],\
              [0,(-0.5*Db),0,0],       \
              [0,0,(-4*mub*KX2*dimcor*Db),(4*mub*KXZ*dimcor*Db)],\
              [(Cnbdot*Db),0,(4*mub*KXZ*dimcor*Db),(-4*mub*KZ2*dimcor*Db)]])

Q_a = np.array([[-CYb,-CL,(-CYp*dimcor),((-CYr+4*mub)*dimcor)],\
              [0,0,-dimcor,0],\
              [-Clb,0,-Clp*dimcor,-Clr*dimcor],\
              [-Cnb,0,-Cnp*dimcor,-Cnr*dimcor]])

R_a = np.array([[-CYda,-CYdr],\
              [0,0],\
              [-Clda,-Cldr],\
              [-Cnda,-Cndr]])

P_a_inv = np.linalg.inv(P_a)

A_a = np.dot(P_a_inv,Q_a)
B_a = np.dot(P_a_inv,R_a)
C_a = np.identity(4)
D_a = np.zeros((4,2))


Sys_a = ml.ss(A_a,B_a,C_a,D_a)


u = np.vstack(((adefflight[st_interval:end_interval])-(adefflight[st_interval:end_interval][0]),\
              (rdefflight[st_interval:end_interval])-(rdefflight[st_interval:end_interval][0])))
t = time[st_interval:end_interval]

sol_a = ml.lsim(Sys_a,U=np.transpose(-u),T=t)
#sol = ctr.forced_response(Sys_s,U=u,T=t)

if situation ==0 or situation ==1:
    print('Not Asymmetric')

else:
    plt.figure('response')
    plt.plot(sol_a[1],(sol_a[0][:,2]*Radtodeg+(rollrate[st_interval:end_interval][0]*Radtodeg)),label='statespace')
    plt.plot(sol_a[1],rollrate[st_interval:end_interval]*Radtodeg,label='data')
    plt.legend()
    plt.show



eigval_a,eigvec_a = np.linalg.eig(A_a)