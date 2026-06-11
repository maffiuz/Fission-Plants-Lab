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
    HEIGHT = 1.5                    # m
    
    # =========================================
    # Elaboration of experimental data
    # Evaluation of air mass flow rate
    air_flow_rate = data['Air flow rate (Nm3/h)'].values
    air_relative_press = data['Relative pressure in the test section (bar)'].values
    
    # Air density
    air_mass_flow_rate = 1.204*np.sqrt((air_relative_press+1.023)/1.023)*air_flow_rate
    rho_air = air_mass_flow_rate/air_flow_rate
    
    # Water properties
    water = Fluid(FluidsList.Water)
    
    rho_water = np.array([])
    mu_water = np.array([])
    water_mass_flow_rate = np.array([])
    experimental_dp = np.array([])
    
    for i, row in data.iterrows():
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
        
        # Experimental pressure drop
        if row['Type of differential pressure (pC-pD) or (pD-pC)'] == 'pC-pD':
            dp = rho*cs.g*HEIGHT + row['Pressure drop in the pipe (mbar)']*100
        else:
            dp = rho*cs.g*HEIGHT - row['Pressure drop in the pipe (mbar)']*100
            
        experimental_dp = np.append(experimental_dp, dp)
            
    data['Water density (kg/m3)'] = rho_water
    data['Water mass flow rate (kg/s)'] = water_mass_flow_rate
    
    # Air viscosity at 20°C
    mu_air = np.array([Fluid(FluidsList.Air).with_state(Input.density(rho),Input.temperature(20)).dynamic_viscosity for rho in rho_air])
    
    data['Air density (kg/m3)'] = rho_air   
    data['Air mass flow rate (kg/h)'] = air_mass_flow_rate
    
    data['Measured pressure drop (Pa)'] = experimental_dp
    
    # =========================================
    # Comparison with Hewitt-Roberts and Taitel Ducker
    # Hewitt-Roberts    
    water_flow_rate  = water_mass_flow_rate/rho_water
    jg = air_flow_rate/3600/FLOW_AREA
    jl = water_flow_rate/FLOW_AREA 
    
    G_air = air_mass_flow_rate/3600/FLOW_AREA
    G_water = water_mass_flow_rate/FLOW_AREA
    
    data['X coordinate Hewitt-Roberts map'] = jl**2*rho_water
    data['Y coordinate Hewitt-Roberts map'] = jg**2*rho_air
    labels_HR = []
    
    flow_pattern = data['Flow pattern']
    i = 1
    for f in flow_pattern:
        if 'slug' in f.lower() and 'churn' in f.lower():
            labels_HR.append(f'{i}: S/C')
        elif 'annular' in f.lower() and 'churn' in f.lower():
            labels_HR.append(f'{i}: A/C')
        elif 'slug' in f.lower():
            labels_HR.append(f'{i}: S')
        elif 'churn' in f.lower():
            labels_HR.append(f'{i}: C')
        elif 'bubbly' in f.lower():
            labels_HR.append(f'{i}: B')
        elif 'annular' in f.lower():
            labels_HR.append(f'{i}: A')
        
        i += 1

    data['Label Hewitt-Roberts map'] = labels_HR

    # =========================================
    # Evaluation of the void fraction
    
    # Flow quality
    quality = air_mass_flow_rate/(air_mass_flow_rate + np.array(water_mass_flow_rate)*3600)
    data['quality'] = quality
    
    # Experimental data
    Drained_mass = data['Water mass in the pipe (g)'].values/1000
    data['Measured void fraction'] = alpha_experimental =  1 - (Drained_mass + M_RES)/M0
    
    # Homogeneous model
    data['Void fraction - Homogeneous model'] = alpha_homogeneous = 1/(1+(1-quality)/quality * rho_air/rho_water)
    
    # Zivi correlation
    data['Void fraction - Zivi correlation'] = 1/(1+(1-quality)/quality * np.pow(rho_air/rho_water,2/3))
    
    # Chisholm correlation
    S = np.sqrt(1-quality*(1-rho_water/rho_air))
    data['Void fraction - Chisholm correlation'] = alpha_chisholm = 1/(1+(1-quality)/quality * rho_air/rho_water*S)
    
    # CISE correlation
    sigma_water = 0.072     # N/m
    beta = rho_air*quality/(rho_water*quality + rho_air*(1-quality))
    Re = 4*water_mass_flow_rate/mu_water/DIAM_IN/cs.pi
    We = np.pow(water_mass_flow_rate/FLOW_AREA,2)*DIAM_IN/sigma_water/rho_water
    E1 = 1.578*np.pow(Re,-0.19)*np.pow(rho_water/rho_air,0.22)
    E2 = 0.0273*We*np.pow(Re,-0.51)*np.pow(rho_water/rho_air,-0.08)
    y = beta/(1-beta)
    S = 1 + E1*np.pow(y/(1+y*E2)-y*E2,0.5)
    data['Void fraction - CISE correlation'] = alpha_CISE = 1/(1+(1-quality)/quality * rho_air/rho_water*S)
    
    # Drift flux model
    j = jl + jg
    
    # Bubbly flow
    C0 = 1.13
    ugj = 1.41 * np.pow(sigma_water*cs.g*(rho_water-rho_air)/rho_water**2,0.25)
    
    data['Void fraction - Drift flux model - Bubbly flow'] = alpha_DF_bubbly = jg/(C0*j+ugj)
    
    # Plug Flow
    C0 = 1.2
    ugj = 0.35 * np.sqrt((rho_water-rho_air)*cs.g*DIAM_IN/rho_water)
    
    data['Void fraction - Drift flux model - Plug flow'] = alpha_DF_plug = jg/(C0*j+ugj)    
    
    # =========================================
    # Elevation pressure changes
    dp = lambda a_vec: np.array([a*rho_a*cs.g*HEIGHT + (1-a)*rho_w*cs.g*HEIGHT for a,rho_a,rho_w in zip(a_vec,rho_air,rho_water)])
    
    # data['Elevation pressure drop - experimental result (Pa)'] = dp(alpha_experimental)
    data['Elevation pressure drop - Homogenous model (Pa)'] = dp(alpha_homogeneous)
    data['Elevation pressure drop - Chisholm model (Pa)'] = dp(alpha_chisholm)
    data['Elevation pressure drop - CISE model (Pa)'] = dp(alpha_CISE)
    data['Elevation pressure drop - Drift flux - bubbly (Pa)'] = dp(alpha_DF_bubbly)
    data['Elevation pressure drop - Drift flux - plug (Pa)'] = dp(alpha_DF_plug)
    
    # =========================================
    # Single flow pressure drops
    Re_water = G_water*DIAM_IN/mu_water
    Re_air = G_air*DIAM_IN/mu_air
    
    friction_factor = lambda Re_vector: np.array([64.0/Re if Re < 3000 else 0.316 * (Re**(-0.25)) for Re in Re_vector])
    
    f_water = friction_factor(Re_water)
    f_air = friction_factor(Re_air)
    
    dp_water = rho_water*cs.g*HEIGHT + 1/2*f_water*HEIGHT/DIAM_IN*G_water**2/rho_water
    dp_air = rho_air*cs.g*HEIGHT + 1/2*f_air*HEIGHT/DIAM_IN*G_air**2/rho_air
    
    dpdz_water = dp_water/HEIGHT
    dpdz_air = dp_air/HEIGHT
    
    # =========================================
    # Friction pressure drops
    # Homogeneous model
    G = G_air + G_water
    rho_h = np.pow(quality/rho_air + (1-quality)/rho_water, -1)
    mu_h = quality*mu_air + (1-quality)*mu_water
    Re_h = G*DIAM_IN/mu_h
    f_h = friction_factor(Re_h)
    dp_friction_h = 1/2*f_h*HEIGHT/DIAM_IN*G**2/rho_h
    
    data['Friction pressure drop - Homogeneous model (Pa)'] = dp_friction_h

    # Friedel model
    Fr_h = G**2/cs.g/DIAM_IN/rho_h**2
    We_h = G**2*DIAM_IN/sigma_water/rho_h
    f_l0 = friction_factor(G*DIAM_IN/mu_water)
    f_g0 = friction_factor(G*DIAM_IN/mu_air)
    E = np.pow(1-quality,2)+quality**2*rho_water/rho_air*f_g0/f_l0
    F = np.pow(quality, 0.78)*np.pow(1-quality,0.224)
    H = np.pow(rho_water/rho_air,0.91)*np.pow(mu_air/mu_water,0.19)*np.pow(1-mu_air/mu_water,0.7)
    phi_l0_squared = E + (3.24*F*H)/(np.pow(Fr_h,0.045)*np.pow(We_h,0.035))
    dp_l0 = 1/2*f_l0*HEIGHT/DIAM_IN*G**2/rho_water
    dp_friction_friedel = dp_l0*phi_l0_squared
    
    data['Friction pressure drops - Friedel model (Pa)'] = dp_friction_friedel
    
    # =========================================
    # Plot data
    # TD annular-slugchurn 
    data['X coordinate TD map - annular-slugchurn'] = np.sqrt(dpdz_water/dpdz_air)
    data['Y coordinate TD map - annular-slugchurn'] = jg*rho_air**(1/2)*pow(cs.g*(rho_water-rho_air)*sigma_water,-1/4)
    
    # TD slug-churn 
    data['X coordinate TD map - slug-churn'] = j/pow(cs.g*DIAM_IN,1/2)
    data['Y coordinate TD map - slug-churn'] = data['Measured void fraction']
    
    # TD bubbly-slugchurn 
    data['X coordinate TD map - bubbly-slugchurn'] = jg*rho_water**(1/2)*pow(cs.g*(rho_water-rho_air)*sigma_water,-1/4)
    data['Y coordinate TD map - bubbly-slugchurn'] = jl/jg
    
    # =========================================
    # Output
    data.to_csv('data/output.csv',index=False, float_format='%.5f')
    
    # =========================================
    # Plots
    plot_HR()
    plot_VF()
    plot_TD_annular_slugchurn()
    plot_TD_slugs_churn()
    plot_TD_bubbly_slugchurn()
    plot_dp()
    
if __name__ == '__main__':
    main()
    plt.show()