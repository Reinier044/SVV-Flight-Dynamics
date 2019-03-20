import numpy as np
from Cit_par import *
import control.matlab as ml
import matplotlib.pyplot as plt
import Flight_data
#Symmetric Flight ____________________________________________________________

x_u = (V0*CXu)/(c*2*muc)
x_alpha = (V0*CXa)/(c*2*muc)
x_theta = (V0*CZ0)/(c*2*muc)
x_q = (V0*CXq)/(c*2*muc)
x_delta_e = (V0*CXde)/(c*2*muc)

z_u = (V0*CZu)/(c*(2*muc-CZadot))
z_alpha = (V0*CZa)/(c*(2*muc-CZadot))
z_theta = -(V0*CX0)/(c*(2*muc-CZadot))
z_q = (V0*(2*muc+CZq))/(c*(2*muc-CZadot))
z_delta_e = (V0*CZde)/(c*(2*muc-CZadot))

m_u = (V0*(Cmu+CZu*(Cmadot/(2*muc-CZadot))))/(c*2*muc*KY2)
m_alpha = (V0*(Cma+CZa*(Cmadot/(2*muc-CZadot))))/(c*2*muc*KY2)
m_theta = -(V0*(CX0*(Cmadot/(2*muc-CZadot))))/(c*2*muc*KY2)
m_q = (V0*(Cmq+Cma*((2*muc+CZq)/(2*muc-CZadot))))/(c*2*muc*KY2)
m_delta_e = (V0*(Cmde+CZde*((Cmadot)/(2*muc-CZadot))))/(c*2*muc*KY2)

A_s = np.array([[x_u,x_alpha,x_theta,x_q   ],\
                [z_u,z_alpha,z_theta,z_q   ],\
                [0  ,0      ,0      ,(V0/c)],\
                [m_u,m_alpha,m_theta,m_q   ]])

B_s = np.array([[x_delta_e],\
                [z_delta_e],\
                [0        ],\
                [m_delta_e]])

C_s = np.identity(4)

D_s = np.zeros((4,1))

Sys_s = ml.ss(A_s,B_s,C_s,D_s)

duration_shp = 50
u = eldefflight[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]*(np.pi/180)
t = time[((st_shp-9)*10):((st_shp-9+duration_shp)*10+1)]

sol = ml.lsim(Sys_s,U=u,T=t)


plt.figure('response')
plt.plot(sol[1],(sol[0][:,2]*(180/np.pi)))
plt.show

eigval_a,eigvec_a = np.linalg.eig(A_s)