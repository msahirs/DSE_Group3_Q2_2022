import numpy
import math
from matplotlib import pyplot as plt


class solar_atmosphere():

    def __init__(self) -> None:

        ## -- Start Constant Zone -- ##
        
        # Solar irradiance at exospheric conditions
        self.I_MAX = 1361.

        # Averaged Earth-Sun Orbit eccentricity over a year
        self.EARTH_ECC = 0.0016708 

        # Atmospheric transmittance factor (generally between 0.6 and 0.7)
        self.ATM_TRANS = 0.65

        ## -- End Constant Zone -- ##
        

        ## -- Init Sun-based variables -- ##

        # Solar elevation angle
        self.omega = 0

        # Slope relative to ground plane
        self.theta_i = 0

        # Day
        self.day = 0


        ## -- End Sun-based variables -- ##


        ## -- Start local-based variables -- ##

        # Incidence Angle
        self.beta_i = 0

        # Air mass ratio
        self.pressure_ratio = 0

        ## -- End local-based variables -- ##


    def set_angles(self,omega,theta_i, beta_i):
        self.omega, self.theta_i, self.beta_i = omega, theta_i, beta_i

    def set_pressure_ratio(self,pressure_ratio):
        self.pressure_ratio = pressure_ratio

    def set_day(self,day):
        self.day = day

    def get_direct_radiance(self):

        I_dn = self.calc_direct_flux()
    
        return I_dn * math.sin(self.omega) * math.cos(self.beta_i)
        
    def get_diffuse_radiance(self):

        I_dh = self.calc_diffuse_flux()
        
        return I_dh * (0.5 + 0.5 * math.cos(self.theta_i))
    
    def get_reflect_radiance(self):

        I_dh = self.calc_diffuse_flux()
        I_dn = self.calc_direct_flux()


        return (I_dn * math.sin(self.omega) + I_dh)*(0.5 - 0.5 * math.cos(self.theta_i))

    def get_total_radiance(self):
        
        solar_sum = self.get_direct_radiance() + self.get_diffuse_radiance() \
                                        + self.get_reflect_radiance()
        
        return solar_sum

    def calc_direct_flux(self):

        I_dn = self.I_MAX * ((1 + self.EARTH_ECC * math.cos(self.calc_true_anomaly())) \
                                            / (1 - self.EARTH_ECC ** 2))**2 \
                                            * (self.ATM_TRANS ** self.calc_air_mass_frac())
        return I_dn

    def calc_diffuse_flux(self):

        I_dn = self.calc_direct_flux()

        sun_elev = math.sin(self.omega)

        if sun_elev < 0: return 0.

        i_dh = 0.5 * I_dn * sun_elev * ((1 - self.ATM_TRANS ** self.calc_air_mass_frac()) \
                                                / (1 - 1.4 * math.log(self.ATM_TRANS)))
        
        return i_dh                                        

    def calc_air_mass_frac(self):
        
        air_mass_frac = self.pressure_ratio * (math.sqrt(1229 + (614 * math.sin(self.omega))**2) \
                                                                - 614 * math.sin(self.omega))
        # print(air_mass_frac)
        return air_mass_frac

    def calc_true_anomaly(self):

        mean_anomaly = self.calc_mean_anomaly()

        true_anomaly = mean_anomaly + (2 * self.EARTH_ECC - 0.25*self.EARTH_ECC**3) * math.sin(mean_anomaly) \
                        + 1.25 * (self.EARTH_ECC ** 2) * math.sin(2 * mean_anomaly) + (13/12) * (self.EARTH_ECC**3)\
                            * math.sin(3*mean_anomaly)

        return true_anomaly

    def calc_mean_anomaly(self):
        
        return (2 * math.pi * self.day) / 365.


# a = solar_atmosphere()

# omega = math.radians(90-6.814)
# beta = math.radians(180+6.814)
# theta = math.radians(180)

# a.set_angles(omega,theta,beta)

# a.set_pressure_ratio(0.054)

# a.set_day(172)

# b = a.get_total_radiance()

def get_flux(zenith,incidence,slope,p_ratio,day):
    
    
    
    atmos = solar_atmosphere()
    

    omega = math.radians(90-zenith)
    beta = math.radians(incidence)
    theta = math.radians(slope)

    atmos.set_angles(omega,theta,beta)

    atmos.set_pressure_ratio(p_ratio)

    atmos.set_day(day)

    net_flux = atmos.get_total_radiance()

    return net_flux