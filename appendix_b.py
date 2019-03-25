import math
from Constantsdictonary import Constants
import numpy as np


W = 60000  # total weight
W_s = 60500  # 'reduced'  weight
m_dot_per_engine = 0.048  # standard fuel flow per engine kg/s

# h_p = 1
# T_m = 1

# TO BE IMPLEMENTED
C_m_delta = 1
C_m_0 = 1
C_m_alpha = 1
alpha = 1
alpha_0 = 0
C_m_delta_f = 1
delta_f = 1
C_m_T_c = 1
T_c = 1
T_c_s = 1
C_m_lg = 1


# TO BE IMPLEMENTED

def elevator_trim():
    deflection_elev = - 1 / C_m_delta * (
            C_m_0 + C_m_alpha * (alpha - alpha_0) + C_m_delta_f * delta_f + C_m_T_c * T_c + C_m_lg)

    deflection = 1
    return deflection_elev


def eq_speed(h_p,T_m,Constants,Vcal,P0rot,rho0rot):
    p = P0rot*(1+ \
                 ((Constants['lmbdaISA']*h_p)/Constants['T_0ref']))\
                 ** (-Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))  # static pressure  
    mach = (2 / (Constants["gammaair"] - 1) * ((1 + P0rot / p * ((1 + (Constants["gammaair"] - 1) / (2 * Constants["gammaair"]) * rho0rot / P0rot * Vcal ** 2) ** (Constants["gammaair"] / (Constants["gammaair"] - 1)) - 1)) ** ((Constants["gammaair"] - 1) / Constants["gammaair"]) - 1)) ** (1 / 2)
    T = T_m / (1 + (Constants["gammaair"] - 1) / 2 * mach ** 2)  # static air temperature
    sound_speed = (Constants["gammaair"] * Constants["Rgas"] * T) ** (1 / 2)  # speed ot sound
    
    V_t = mach * sound_speed
    return V_t,mach,p

def non_standard_mass(V_e):
    # reduced speed due to non_standard mass
    V_e_tilda = V_e * (W_s / W) ** (1 / 2)
    return V_e_tilda


def non_standard_engine_thrust(measured_trirm):
    deflection_elev = elevator_trim()

    # reduced elevator deflection
    reduced_deflection = measured_trirm - 1 / C_m_delta*C_m_T_c*(T_c_s-T_c)
