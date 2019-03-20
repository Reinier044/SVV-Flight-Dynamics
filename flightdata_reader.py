import scipy.io as spio
from Stat1 import Stat1Results 
'''
To use:
copy paste the following:
    ============================================
    import flightdata_reader
    
    flightdata = flightdata_reader.flightdata
    ============================================
This python file read the flightdata.mat file and convert it to python dictionary.
Call each variable using the following steps (example angle of attack):
    =============================================
    AoA = flightdata['flightdata']['vane_AOA']['data']
    =============================================
List of variable names to be called are in the bottom of this python file.
'''
# ==========Definitions===============


def loadmat(filename):
    data = spio.loadmat(filename, struct_as_record=False, squeeze_me=True)
    return _check_keys(data)


def _check_keys(dict):
    for key in dict:
        if isinstance(dict[key], spio.matlab.mio5_params.mat_struct):
            dict[key] = _todict(dict[key])
    return dict


def _todict(matobj):
    dict = {}
    for strg in matobj._fieldnames:
        elem = matobj.__dict__[strg]
        if isinstance(elem, spio.matlab.mio5_params.mat_struct):
            dict[strg] = _todict(elem)
        else:
            dict[strg] = elem
    return dict


DataBook = Stat1Results["DataBook"]

if DataBook == "R":
    flightdata = loadmat('Refdata.mat')
    
else:
    flightdata = loadmat('FTISxprt-20190307_124723.mat')

# AoA = flightdata['flightdata']['vane_AOA']['data']
# print(AoA)

'''
Content of the dictionary:
                 vane_AOA: [1×1 struct]     Angle of Attack [deg]
             elevator_dte: [1×1 struct]     Deflection of Elevator dte [deg]
                column_fe: [1×1 struct]     Force elevator control wheel (Fe) [N]
            lh_engine_FMF: [1×1 struct]     Fuel Mass Flow Left [lbs/hr]
            rh_engine_FMF: [1×1 struct]     Fuel Mass Flow  Right [lbs/hr]
            lh_engine_itt: [1×1 struct]     Inter Turbine Temperature Left  [deg C]
            rh_engine_itt: [1×1 struct]     Inter Turbine Temperature Right [deg C]
             lh_engine_OP: [1×1 struct]     Oil Pressure Left  [psi]
             rh_engine_OP: [1×1 struct]     oil Pressure Right [psi]
                column_Se: [1×1 struct]     Deflection of control column (Se) [deg]
         lh_engine_fan_N1: [1×1 struct]     Fan Speed Left [%]
     lh_engine_turbine_N2: [1×1 struct]     Turbine Speed Left [%]
         rh_engine_fan_N1: [1×1 struct]     Fan Speed Right [%]
     rh_engine_turbine_N2: [1×1 struct]     Turbine Speed Right [%]
             lh_engine_FU: [1×1 struct]     Calculated Fuel Used by Mass Flow Left[lbs]
             rh_engine_FU: [1×1 struct]     Calculated Fuel Used by Mass Flow Right[lbs]
                  delta_a: [1×1 struct]     Deflection Aileron (da) [deg]
                  delta_e: [1×1 struct]     Deflection Elevator (de) [deg
                  delta_r: [1×1 struct]     Deflection Rudder [deg]
                 Gps_date: [1×1 struct]     Date of gpd [ddmmyy]
               Gps_utcSec: [1×1 struct]     UTC Seconds [sec]
               Ahrs1_Roll: [1×1 struct]     Roll Angle [deg]
              Ahrs1_Pitch: [1×1 struct]     Pitch Angle [deg]
         Fms1_trueHeading: [1×1 struct]     True Heading [no unit]
                  Gps_lat: [1×1 struct]     GNSS Latitude [deg]
                 Gps_long: [1×1 struct]     GNSS Longitude [deg]
          Ahrs1_bRollRate: [1×1 struct]     Body Roll Rate [deg/s]
         Ahrs1_bPitchRate: [1×1 struct]     Body Pitch Rate [deg/s]
           Ahrs1_bYawRate: [1×1 struct]     Body Yaw rate [deg/s]
           Ahrs1_bLongAcc: [1×1 struct]     Body Long. Acceleration [g]
            Ahrs1_bLatAcc: [1×1 struct]     Body Lat. Acceleration [g]
           Ahrs1_bNormAcc: [1×1 struct]     Body Normal Acceleration [g]
            Ahrs1_aHdgAcc: [1×1 struct]     Along Heading Acceleration [g]
            Ahrs1_xHdgAcc: [1×1 struct]     Cross Heading Acceleration [g]
            Ahrs1_VertAcc: [1×1 struct]     vertical Acceleration [g]
                Dadc1_sat: [1×1 struct]     Static Air Temperature [deg C]
                Dadc1_tat: [1×1 struct]     Total Air Temperature [deg C]
                Dadc1_alt: [1×1 struct]     Pressure Altitude (1013.25 mB) [ft]
              Dadc1_bcAlt: [1×1 struct]     Baro Corrected Altitude #1 [ft]
            Dadc1_bcAltMb: [1×1 struct]     No desc, no units, all zero []
               Dadc1_mach: [1×1 struct]     Mach []
                Dadc1_cas: [1×1 struct]     Computed Airspeed [kts]
                Dadc1_tas: [1×1 struct]     True Airspeed [kts]
            Dadc1_altRate: [1×1 struct]     Altitude Rate [ft/min]
      measurement_running: [1×1 struct]     Measurement Running []
        measurement_n_rdy: [1×1 struct]     Number of Measurements Ready []
      display_graph_state: [1×1 struct]     Status of Graph []
    display_active_screen: [1×1 struct]     Active Screen []
                     time: [1×1 struct]     Time [sec]
'''
