import numpy as np
from Cit_par import *
import control.matlab as ml
import matplotlib.pyplot as plt
import numpy as np
from Constantsdictonary import Constants

Db = Constants['Span']/V0
dimcor = 0.5*Constants['Span']/V0

y_beta = (V0/b)*(CYb/(2*mub))
y_phi = (V0/b)*(CL/(2*mub))
y_p = (V0/b)*(CYp/(2*mub))
y_r = (V0/b)*((CYr-(4*mub))/(2*mub))
y_da = (V0/b)*(CYda/(2*mub))
y_dr = (V0/b)*(CYdr/(2*mub))

l_beta = (V0/b)*((Clb*KZ2+Cnb*KXZ)/(4*mub*(KX2*KZ2-KXZ**2)))
l_phi = 0
l_p = (V0/b)*((Clp*KZ2+Cnp*KXZ)/(4*mub*(KX2*KZ2-KXZ**2)))
l_r = (V0/b)*((Clr*KZ2+Cnr*KXZ)/(4*mub*(KX2*KZ2-KXZ**2)))
l_da = (V0/b)*((Clda*KZ2+Cnda*KXZ)/(4*mub*(KX2*KZ2-KXZ**2)))
l_dr = (V0/b)*((Cldr*KZ2+Cndr*KXZ)/(4*mub*(KX2*KZ2-KXZ**2)))

n_beta = (V0/b)*((Clb*KXZ+Cnb*KX2)/(4*mub*(KX2*KZ2-KXZ**2)))
n_phi = 0
n_p = (V0/b)*((Clp*KXZ+Cnp*KX2)/(4*mub*(KX2*KZ2-KXZ**2)))
n_r = (V0/b)*((Clr*KXZ+Cnr*KX2)/(4*mub*(KX2*KZ2-KXZ**2)))
n_da = (V0/b)*((Clda*KXZ+Cnda*KX2)/(4*mub*(KX2*KZ2-KXZ**2)))
n_dr = (V0/b)*((Cldr*KXZ+Cndr*KX2)/(4*mub*(KX2*KZ2-KXZ**2)))

<<<<<<< HEAD
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
#
#plt.figure()
#plt.plot(sol[1],sol[0][:,0])
#plt.show
#
=======
#state space matrices xdot = Ax + Bu for assymetric case
A_a = np.array([[y_beta , y_phi , y_p , y_r],\
                [0 , 0 , 2*(V0/b) , 0],\
                [l_beta , 0 , l_p , l_r],\
                [n_beta , 0 , n_p , n_r]])

B_a = np.array([[0 , y_dr],\
                [0 , 0],\
                [l_da , l_dr],\
                [n_da , n_dr]])

C_a = np.identity(4)

D_a = np.zeros((4,2))

Sys_a = ml.ss(A_a,B_a,C_a,D_a)

t = np.arange(0,100,0.1)
u = np.ones((len(t),2))
sol = ml.lsim(Sys_a,U=u,T=t)

plt.figure()
plt.plot(sol[1],sol[0][:,0])
plt.show

>>>>>>> aa8ebd1235800a8c6ba8d1ff1e79497db7df0779
eigval_a,eigvec_a = np.linalg.eig(A_a)