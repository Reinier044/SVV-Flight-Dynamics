import numpy as np
from Cit_par import *
import control.matlab as ml
import control as ctr
import matplotlib.pyplot as plt
from Flight_data import *
import os


from Constantsdictonary import Constants

if not os.path.exists('./Plots'):
    os.makedirs('./Plots')
    
fontx = 8
fonty = 8
fontlegend = 'xx-small'

AoA = AoA - AoA[st_interval]
pitchA = pitchA - pitchA[st_interval]

print(situation)

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

eigval_s,eigvec_s = np.linalg.eig(A_s)

#state space response to flight date input
u = (eldefflight[st_interval:end_interval])-(eldefflight[st_interval:end_interval][0])
t = time[st_interval:end_interval]
t = np.arange(0,t[-1]-t[0]+0.1,0.1)

sol = ml.lsim(Sys_s,U=u,T=t)

if situation ==0:
    
    plt.figure('phugoid')
    plt.subplot(411)
    plt.title("Phugoid")
    plt.plot(sol[1],Vtrue[st_interval:end_interval],label='data')
    plt.plot(sol[1],sol[0][:,0]+(Vtrue[st_interval:end_interval][0]),label='statespace')
    plt.ylabel(r'$V_t$ [m/s]',fontsize = fonty)
    plt.yticks(np.arange(80,130,10),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = 0)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)

##    Constant angle of attack so no interest in this minor deviation
#    plt.figure('response AoA')
#    plt.plot(sol[1],(sol[0][:,1]*Radtodeg+(AoA[st_interval:end_interval][0])*Radtodeg),label='statespace')
#    plt.plot(sol[1],AoA[st_interval:end_interval]*Radtodeg,label='data')
#    plt.legend()
#    plt.show
    
    plt.subplot(412)
    plt.plot(sol[1],pitchA[st_interval:end_interval],label='data')
    plt.plot(sol[1],(sol[0][:,2]+pitchA[st_interval:end_interval][0]),label='statespace')
    plt.ylabel(r'$\theta$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.15,0.20,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = 0)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
   
    plt.subplot(413)
    plt.plot(sol[1],pitchrate[st_interval:end_interval],label='data')
    plt.plot(sol[1],(sol[0][:,3]+pitchrate[st_interval:end_interval][0]),label='statespace',)
    plt.ylabel(r'q [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.030,0.035,0.01),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = 0)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(414)
    plt.plot(sol[1],eldefflight[st_interval:end_interval]-eldefflight[st_interval:end_interval][0],label='data')
    plt.ylabel(r'$\delta_e$ [rad]',fontsize = fonty)
    plt.xlabel(r'time [sec]')
    plt.yticks(np.arange(-0.01,0.015,0.005),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = fontx)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    plt.show
    
    plt.savefig('./Plots/Phugoid.pdf')
#    plt.close()

elif situation ==1:
    

##  Speed is neglected to change much
#    plt.figure()
#    plt.plot(sol[1],Vtrue[st_interval:end_interval],label='data')
#    plt.plot(sol[1],(sol[0][:,0]+(Vtrue[st_interval:end_interval][0])),label='statespace')
#    plt.ylabel(r'$V_t$ [m/s]',fontsize = fonty)
#    plt.yticks(fontsize = fonty)
#    plt.xticks(fontsize = 0)
#    plt.grid()
#    plt.legend(loc = 1,fontsize ='xx-small')
    
    plt.figure('Short period')
    plt.subplot(411)
    plt.title('Short Period')
    plt.plot(sol[1],AoA[st_interval:end_interval],label='data')
    plt.plot(sol[1],sol[0][:,1]+(AoA[st_interval:end_interval][0]),label='statespace')
    plt.ylabel(r'$\alpha$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.01,0.06,0.01),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(412)
    plt.plot(sol[1],pitchA[st_interval:end_interval],label='data')
    plt.plot(sol[1],sol[0][:,2]+(pitchA[st_interval:end_interval][0]),label='statespace')
    plt.ylabel(r'$\theta$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(0,0.35,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(413)
    plt.plot(sol[1],pitchrate[st_interval:end_interval],label='data')
    plt.plot(sol[1],sol[0][:,3]+(pitchrate[st_interval:end_interval][0]),label='statespace')
    plt.ylabel(r'q [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.05,0.125,0.025),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(414)
    plt.plot(sol[1],eldefflight[st_interval:end_interval]-(eldefflight[st_interval:end_interval][0]),label='data')
    plt.ylabel(r'$V_t$ [m/s]',fontsize = fonty)
    plt.xlabel(r'time [sec]')
    plt.yticks(np.arange(-0.03,0.02,0.01),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = fontx)
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    plt.show()
    
    plt.savefig('./Plots/Shortperiod.pdf')
#    plt.close()

else:
    print('Not Symmetric')
    

#state space initial value problem
sol1 = ctr.step_response(Sys_s,t,X0 = np.array([[0],[0.1],[0],[0]]))

plt.figure('initial')
plt.subplot(411)
plt.plot(sol1[0],sol1[1][0,:])

plt.subplot(412)
plt.plot(sol1[0],sol1[1][1,:])

plt.subplot(413)
plt.plot(sol1[0],sol1[1][2,:])

plt.subplot(414)
plt.plot(sol1[0],sol1[1][3,:])












