import pandas as pd
import scipy.constants as cs
import numpy as np
from pyfluids import Fluid, FluidsList, Input
from plotters import *

def main():
    data = pd.read_csv('data/data.csv')
    
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
    # 1- Comparison with Hewitt-Roberts and Taitel Ducker
    # Hewitt-Roberts    
    water_flow_rate  = water_mass_flow_rate/rho_water
    jg = air_flow_rate/3600/FLOW_AREA
    jl = water_flow_rate/FLOW_AREA 
    
    G_air = air_mass_flow_rate/3600/FLOW_AREA
    G_water = water_mass_flow_rate/FLOW_AREA
    
    X_coord_HR = G_water**2/rho_water
    Y_coord_HR = G_air**2/rho_air
    labels_HR = []
    
    flow_pattern = data['Flow pattern']
    for f in flow_pattern:
        if 'slug' in f.lower() and 'churn' in f.lower():
            labels_HR.append('S/C')
        elif 'annular' in f.lower() and 'churn' in f.lower():
            labels_HR.append('A/C')
        elif 'slug' in f.lower():
            labels_HR.append('S')
        elif 'churn' in f.lower():
            labels_HR.append('C')
        elif 'bubbly' in f.lower():
            labels_HR.append('B')
        elif 'annular' in f.lower():
            labels_HR.append('A')

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
    
    # Drift flux model
    j = jl + jg
    
    # Bubbly flow
    C0 = 1.13
    ugj = 1.41 * np.pow(sigma_water*cs.g*(rho_water-rho_air)/rho_water**2,0.25)
    
    data['Void fraction - Drift flux model - Bubbly flow'] = jg/(C0*j+ugj)
    
    # Plug Flow
    C0 = 1.2
    ugj = 0.35 * np.sqrt((rho_water-rho_air)*cs.g*DIAM_IN/rho_water)
    
    data['Void fraction - Drift flux model - Plug flow'] = jg/(C0*j+ugj)
    
    # Output
    data.to_csv('data/output.csv',index=False, float_format='%.5f')
    
    # Plots
    plot_HR(X_coord_HR,Y_coord_HR,labels_HR)
    
if __name__ == '__main__':
    main()