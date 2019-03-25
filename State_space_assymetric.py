import numpy as np
from Cit_par import *
import control.matlab as ml
import matplotlib.pyplot as plt
import numpy as np
from Constantsdictonary import Constants
from Flight_data import *
import os

if not os.path.exists('./Plots'):
    os.makedirs('./Plots')
    
fontx = 8
fonty = 8
fontlegend = 'xx-small'

print(situation)

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

eigval_a,eigvec_a = np.linalg.eig(A_a)

u = np.vstack(((adefflight[st_interval:end_interval])-(adefflight[st_interval:end_interval][0]),\
              (rdefflight[st_interval:end_interval])-(rdefflight[st_interval:end_interval][0])))


t = time[st_interval:end_interval]
t = np.arange(0,t[-1]-t[0]+0.1,0.1)


sol_a = ml.lsim(Sys_a,U=np.transpose(-u),T=t)
#sol = ctr.forced_response(Sys_s,U=u,T=t)

if situation ==0 or situation ==1:
    print('Not Asymmetric')

elif situation ==2:
    
    plt.subplot(411)
    plt.title('Dutch Roll, No yaw damper')
    plt.plot(sol_a[1],rollA[st_interval:end_interval],label='data')    
    plt.plot(sol_a[1],(sol_a[0][:,1]+(rollA[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$\phi$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.2,0.15,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(412)
    plt.plot(sol_a[1],rollrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],(sol_a[0][:,2]+(rollrate[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$p$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.3,0.4,0.1),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(413)
    plt.plot(sol_a[1],yawrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],(sol_a[0][:,3]+(yawrate[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$r$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.3,0.4,0.1),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)

    plt.subplot(414)
    plt.plot(sol_a[1],(adefflight[st_interval:end_interval])-(adefflight[st_interval:end_interval][0]),label='data')
    plt.plot(sol_a[1],(rdefflight[st_interval:end_interval])-(rdefflight[st_interval:end_interval][0]),label='data')
    plt.ylabel(r'$\delta_a , \delta_r$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.15,0.2,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = fontx)
    plt.xlabel(r'time [sec]')
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.savefig('./Plots/Dutchrollnodamper.pdf')
#    plt.close()

elif situation ==3:
    
    plt.subplot(411)
    plt.title('Dutch Roll, with yaw damper')
    plt.plot(sol_a[1],rollA[st_interval:end_interval],label='data')    
    plt.plot(sol_a[1],(sol_a[0][:,1]+(rollA[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$\phi$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.2,0.15,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(412)
    plt.plot(sol_a[1],rollrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],(sol_a[0][:,2]+(rollrate[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$p$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.3,0.4,0.1),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(413)
    plt.plot(sol_a[1],yawrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],(sol_a[0][:,3]+(yawrate[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$r$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.3,0.4,0.1),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)

    plt.subplot(414)
    plt.plot(sol_a[1],(adefflight[st_interval:end_interval])-(adefflight[st_interval:end_interval][0]),label='a')
    plt.plot(sol_a[1],(rdefflight[st_interval:end_interval])-(rdefflight[st_interval:end_interval][0]),label='r')
    plt.ylabel(r'$\delta_a , \delta_r$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.15,0.2,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = fontx)
    plt.xlabel(r'time [sec]')
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.savefig('./Plots/Dutchrolldamper.pdf')
#    plt.close()
    
elif situation ==4:
    
    plt.subplot(411)
    plt.title('Aperiodic roll')
    plt.plot(sol_a[1],rollA[st_interval:end_interval],label='data')    
    plt.plot(sol_a[1],(sol_a[0][:,1]+(rollA[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$\phi$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.75,1.25,0.25),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(412)
    plt.plot(sol_a[1],rollrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],(sol_a[0][:,2]+(rollrate[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$p$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.3,0.4,0.1),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(413)
    plt.plot(sol_a[1],yawrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],(sol_a[0][:,3]+(yawrate[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$r$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.3,0.4,0.1),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)

    plt.subplot(414)
    plt.plot(sol_a[1],(adefflight[st_interval:end_interval])-(adefflight[st_interval:end_interval][0]),label='a')
    plt.plot(sol_a[1],(rdefflight[st_interval:end_interval])-(rdefflight[st_interval:end_interval][0]),label='r')
    plt.ylabel(r'$\delta_a , \delta_r$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.10,0.15,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+1,1),fontsize = fontx)
    plt.xlabel(r'time [sec]')
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.savefig('./Plots/Aperiodicroll.pdf')
#    plt.close()
    
elif situation ==5:
    
    plt.subplot(411)
    plt.title('Spiral')
    plt.plot(sol_a[1],rollA[st_interval:end_interval],label='data')    
    plt.plot(sol_a[1],(sol_a[0][:,1]+(rollA[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$\phi$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-1,0.5,0.25),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(412)
    plt.plot(sol_a[1],rollrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],(sol_a[0][:,2]+(rollrate[st_interval:end_interval][0])),label='statespace')
    plt.ylabel(r'$p$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.1,0.15,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.subplot(413)
    plt.plot(sol_a[1],yawrate[st_interval:end_interval],label='data')
    plt.plot(sol_a[1],sol_a[0][:,3]+(yawrate[st_interval:end_interval][0]),label='statespace')
    plt.ylabel(r'$r$ [rad/sec]',fontsize = fonty)
    plt.yticks(np.arange(-0.1,0.15,0.05),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = 0)
    plt.xlim(t[0],t[-1])
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)

    plt.subplot(414)
    plt.plot(sol_a[1],(adefflight[st_interval:end_interval])-(adefflight[st_interval:end_interval][0]),label='data')
    plt.plot(sol_a[1],(rdefflight[st_interval:end_interval])-(rdefflight[st_interval:end_interval][0]),label='data')
    plt.ylabel(r'$\delta_a , \delta_r$ [rad]',fontsize = fonty)
    plt.yticks(np.arange(-0.01,0.015,0.005),fontsize = fonty)
    plt.xticks(np.arange(0,t[-1]+25,25),fontsize = fontx)
    plt.xlim(t[0],t[-1])
    plt.xlabel(r'time [sec]')
    plt.grid()
    plt.legend(loc = 1,fontsize = fontlegend)
    
    plt.savefig('./Plots/spiral.pdf')
#    plt.close()
    
##state space initial value problem
#tinitial = np.arange(0,10,0.001)
#sol1 = ml.lsim(Sys_a,T=tinitial,X0 = np.array([[0.0],[0.0],[0.0],[0.05]]))
#
#plt.figure('initial value problem')
#plt.subplot(411)
#plt.plot(sol1[1],sol1[0][:,0])
#plt.ylabel(r'$\beta$ [rad]',fontsize = fonty)
#plt.yticks(np.arange(-0.04,0.05,0.02),fontsize = fonty)
#plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
#plt.xlim(tinitial[0],tinitial[-1])
#plt.grid()
#
#plt.subplot(412)
#plt.plot(sol1[1],sol1[0][:,1])
#plt.ylabel(r'$\phi$ [rad]',fontsize = fonty)
#plt.yticks(np.arange(0.0,0.035,0.01),fontsize = fonty)
#plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
#plt.xlim(tinitial[0],tinitial[-1])
#plt.grid()
#
#plt.subplot(413)
#plt.plot(sol1[1],sol1[0][:,2])
#plt.ylabel(r'$p$ [rad/sec]',fontsize = fonty)
#plt.yticks(np.arange(-0.02,0.05,0.02),fontsize = fonty)
#plt.xticks(np.arange(0,t[-1]+1,1),fontsize = 0)
#plt.xlim(tinitial[0],tinitial[-1])
#plt.grid()
#
#plt.subplot(414)
#plt.plot(sol1[1],sol1[0][:,3])
#plt.ylabel(r'$r$ [rad/sec]',fontsize = fonty)
#plt.xlabel(r'time [sec]')
#plt.yticks(np.arange(-0.03,0.06,0.02),fontsize = fonty)
#plt.xticks(np.arange(0,t[-1]+1,1),fontsize = fontx)
#plt.xlim(tinitial[0],tinitial[-1])
#plt.grid()
