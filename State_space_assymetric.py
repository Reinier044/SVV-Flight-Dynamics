import numpy as np
from Cit_par import *
import control.matlab as ml
import matplotlib.pyplot as plt
import numpy as np
from Constantsdictonary import Constants

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



#Sys_a = ml.ss(A_a,B_a,C_a,D_a)
#
#t = np.arange(0,100,0.1)
#u = np.ones((len(t),2))
#sol = ml.lsim(Sys_a,U=u,T=t)
#
#plt.figure()
#plt.plot(sol[1],sol[0][:,0])
#plt.show


eigval_a,eigvec_a = np.linalg.eig(A_a)