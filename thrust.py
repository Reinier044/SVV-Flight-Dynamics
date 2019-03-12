T_temp = 10  # actual outside temperature
T_temp_isa = 9  # isa measurement on altitude
bypass_ratio = 2.6

#RATIO BETWEEN THE 2 IS ASSUMED CONSTANT
mdot_fuel = 0.177  # fuel flow
mdot_tot = 35.245  # total flow


H = 1  # heat value CONSTANT
eta_tot = 1  # efficiency CONSTANT


# YET TO IMPLEMENT
w_e_core = 1 # exit airspeed engine core
w_e_fan = 1 # exit airspeed fan
V_0 = 1 # undistributed air speed

def thrust(Gamma, mach, altitude):
    delta_T_temp = T_temp - T_temp_isa
    mdot_core = 1/(bypass_ratio+1)*mdot_fuel
    mdot_fan = bypass_ratio/(bypass_ratio+1)*mdot_fuel
    w_e_mean = 1/(bypass_ratio+1)*w_e_core+bypass_ratio/(bypass_ratio+1)*w_e_fan


    T_p = mdot_fuel*(w_e_mean-V_0)
