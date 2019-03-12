import math
import Constants

W = 60000  # total weight
V_c = 128.09667  # measured calibrated air speed
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


def eq_speed(h_p, T_m,Constants):
    p = Constants['p_oISA']*(1+ \
                 ((Constants['lmbdaISA']*h_p)/Constants['T_0ISA']))\
                 ** (-Constants['g_0']/(Constants['Rgas']*Constants['lmbdaISA']))  # static pressure
    
    mach = (2 / (gamma - 1) * ((1 + p_0 / p * ((1 + (gamma - 1) / (2 * gamma) * rho_0 / p_0 * V_c ** 2) ** (gamma / (gamma - 1)) - 1)) ** ((gamma - 1) / gamma) - 1)) ** (1 / 2)
    print(mach)
    T = T_m / (1 + (gamma - 1) / 2 * mach ** 2)  # static air temperature
    sound_speed = (gamma * R * T) ** (1 / 2)  # speed ot sound
    rho = p / R / T  # air density
    V_e = mach * sound_speed * (rho / rho_0) ** (1 / 2)

    return V_e


# print(eq_speed(1527.048,12.5))
V_e = eq_speed(1527.048, 12.5)  # V_e for non_standrad mass


def non_standard_mass(V_e):
    # reduced speed due to non_standard mass
    V_e_tilda = V_e * (W_s / W) ** (1 / 2)
    return V_e_tilda


def non_standard_engine_thrust(measured_trirm):
    deflection_elev = elevator_trim()

    # reduced elevator deflection
    reduced_deflection = measured_trirm - 1 / C_m_delta*C_m_T_c*(T_c_s-T_c)
