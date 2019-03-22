import numpy as np
from Cit_par import *
import control.matlab as ml
import control as ctr
import matplotlib.pyplot as plt
from Flight_data import *

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

u = (eldefflight[st_interval:end_interval])-(eldefflight[st_interval:end_interval][0])
t = time[st_interval:end_interval]

sol = ml.lsim(Sys_s,U=u,T=t)
print(situation)

AoA = AoA - AoA[st_interval]
pitchA = pitchA - pitchA[st_interval]

#sol = ctr.forced_response(Sys_s,U=u,T=t)

if situation ==0 or situation ==1:
    plt.figure('response speed')
    plt.plot(sol[1],(sol[0][:,0]+(Vtrue[st_interval:end_interval][0])),label='statespace')
    plt.plot(sol[1],Vtrue[st_interval:end_interval],label='data')
    plt.legend()
    plt.show
    
    plt.figure('response AoA')
    plt.plot(sol[1],(sol[0][:,1]*Radtodeg+(AoA[st_interval:end_interval][0])*Radtodeg),label='statespace')
    plt.plot(sol[1],AoA[st_interval:end_interval]*Radtodeg,label='data')
    plt.legend()
    plt.show
    
    plt.figure('response pitch')
    plt.plot(sol[1],(sol[0][:,2]*Radtodeg+(pitchA[st_interval:end_interval][0])*Radtodeg),label='statespace')
    plt.plot(sol[1],pitchA[st_interval:end_interval]*Radtodeg,label='data')
    plt.legend()
    plt.show
    
    plt.figure('response Pitch rate')
    plt.plot(sol[1],(sol[0][:,3]*Radtodeg+(pitchrate[st_interval:end_interval][0])*Radtodeg),label='statespace')
    plt.plot(sol[1],pitchrate[st_interval:end_interval]*Radtodeg,label='data')
    plt.legend()
    plt.show
    
    plt.figure('Elevator defl')
    plt.plot(sol[1],eldefflight[st_interval:end_interval]*Radtodeg-(eldefflight[st_interval:end_interval][0])*Radtodeg,label='data')
    plt.legend()
    plt.show
else:
    print('Not Symmetric')
eigval_s,eigvec_s = np.linalg.eig(A_s)