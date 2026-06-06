import pandas as pd
import scipy.constants as cs
import numpy as np
from pyfluids import Fluid, FluidsList, Input

def main():
    data = pd.read_csv('data.csv')
    
    # Constants
    DIAM_IN = 0.026                 # m, pipe inner diameter
    FLOW_AREA = DIAM_IN**2/4*cs.pi  # m2, flow cross section
    M0 = 1.014                      # kg
    M_RES = 0.116                   # kg
    
    # Water properties
    water = Fluid(FluidsList.Water)
    
    rho_water = np.array([])
    mu_water = np.array([])
    water_mass_flow_rate = np.array([])
    
    for _, row in data.iterrows():
        # Properties for each state
        Temperature = row['Water temperature (C)']
        actual_water = water.with_state(Input.temperature(Temperature), Input.pressure(cs.atm))
        rho = actual_water.density
        
        rho_water = np.append(rho_water,rho)
        mu_water = np.append(mu_water, actual_water.dynamic_viscosity)
                
        # Evaluation of water mass flow rate 
        DeltaP = row['Water diaphragm press. drop (mbar)']*100 # Pa
        
        if row['Water diaphram'] == 'S':
            rate = 0.650729*cs.pi*0.0084**2/4*np.sqrt(2*rho*DeltaP)+0.01415274
        else:
            rate = 0.728193*cs.pi*0.0153**2/4*np.sqrt(2*rho*DeltaP)+0.00375718
            
        water_mass_flow_rate = np.append(water_mass_flow_rate, rate)
            
    data['Water density (kg/m3)'] = rho_water
    data['Water mass flow rate (kg/s)'] = water_mass_flow_rate
            
    
    # Evaluation of air mass flow rate
    air_flow_rate = data['Air flow rate (Nm3/h)'].values
    air_relative_press = data['Relative pressure in the test section (bar)'].values
    
    # Air density
    air_mass_flow_rate = 1.204*np.sqrt((air_relative_press+1.023)/1.023)*air_flow_rate
    rho_air = air_mass_flow_rate/air_flow_rate
    
    data['Air density (kg/m3)'] = rho_air   
    data['Air mass flow rate (kg/h)'] = air_mass_flow_rate
    
    # =========================================
    # Evaluation of the void fraction
    
    # Flow quality
    quality = air_mass_flow_rate/(air_mass_flow_rate + np.array(water_mass_flow_rate)*3600)
    data['quality'] = quality
    
    # Experimental data
    Drained_mass = data['Water mass in the pipe (g)'].values/1000
    data['Measured void fraction'] = 1 - (Drained_mass + M_RES)/M0
    
    # Homogenous model
    data['Void fraction - Homogenous model'] = 1/(1+(1-quality)/quality * rho_air/rho_water)
    
    # Zivi correlation
    data['Void fraction - Zivi correlation'] = 1/(1+(1-quality)/quality * np.pow(rho_air/rho_water,2/3))
    
    # CISE correlation
    sigma_water = 0.072     # N/m
    beta = rho_air*quality/(rho_water*quality + rho_air*(1-quality))
    Re = 4*water_mass_flow_rate/mu_water/DIAM_IN/cs.pi
    We = np.pow(water_mass_flow_rate/FLOW_AREA,2)*DIAM_IN/sigma_water/rho_water
    E1 = 1.578*np.pow(Re,-0.19)*np.pow(rho_water/rho_air,0.22)
    E2 = 0.0273*We*np.pow(Re,-0.51)*np.pow(rho_water/rho_air,-0.08)
    y = beta/(1-beta)
    S = 1 + E1*np.pow(y/(1+y*E2)-y*E2,0.5)
    data['Void fraction - CISE correlation'] = 1/(1+(1-quality)/quality * rho_air/rho_water*S)
    
    # Output
    data.to_csv('output.csv',index=False, float_format='%.5f')
    
if __name__ == '__main__':
    main()