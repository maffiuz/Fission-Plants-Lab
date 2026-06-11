import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_dp():
    
    data = pd.read_csv('data/output.csv')
    
    dp_experimental_total = data['Measured pressure drop (Pa)']
    dp_homogenous_elv = data['Elevation pressure drop - Homogenous model (Pa)']
    dp_chisholm_elv = data['Elevation pressure drop - Chisholm model (Pa)']
    dp_CISE_elv = data['Elevation pressure drop - CISE model (Pa)']
    dp_DF_bubbly_elv = data['Elevation pressure drop - Drift flux - bubbly (Pa)'] 
    dp_DF_plug_elv = data['Elevation pressure drop - Drift flux - plug (Pa)']
    dp_homogenous_frc = data['Friction pressure drop - Homogeneous model (Pa)']
    dp_friedel_frc = data['Friction pressure drops - Friedel model (Pa)']
    
    dp_total_1 = dp_homogenous_frc + dp_homogenous_elv
    dp_total_2 = dp_friedel_frc + dp_CISE_elv
    dp_total_3 = dp_friedel_frc + dp_chisholm_elv
    dp_total_4 = dp_friedel_frc + dp_DF_bubbly_elv
    dp_total_5 = dp_friedel_frc + dp_DF_plug_elv
    
    diagonal = np.linspace(0,25e3)
    
    plt.figure()
    plt.subplots_adjust(right=0.65)
    
    plt.plot(dp_experimental_total,dp_total_1,'sk ',label='Homogeneous',markersize=6)
    plt.plot(dp_experimental_total,dp_total_2,'d ',color='green',label='Friedel + CISE',markersize=6)
    plt.plot(dp_experimental_total,dp_total_3,'^ ',color='grey',label='Firedel + Chisholm',markersize=6)
    plt.plot(dp_experimental_total,dp_total_4,'x ',color='blue',label='Friedel + Drift (B)',markersize=6)
    plt.plot(dp_experimental_total,dp_total_5,'+ ',color='magenta',label='Friedel + Drift (P)',markersize=6)
    
    plt.plot(diagonal, diagonal, 'r', label='diagonal')
    plt.plot(diagonal, diagonal*1.2, 'r-.', label='+ 20%')
    plt.plot(diagonal, diagonal*0.8, 'r--', label='- 20%')
    
    plt.grid()
    plt.xlim((0,25e3))
    plt.ylim((0,25e3))
    plt.xlabel('Experimental pressure drop (Pa)')
    plt.ylabel('Calculated pressure drop (Pa)')
    
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
        
    
if __name__ == '__main__':
    plot_dp()
    plt.show()