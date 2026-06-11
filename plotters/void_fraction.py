import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def plot_VF():
    
    data = pd.read_csv('data/output.csv')
    
    VF_measured = data['Measured void fraction']
    VF_homogenous = data['Void fraction - Homogeneous model']
    VF_zivi = data['Void fraction - Zivi correlation']
    VF_chisholm = data['Void fraction - Chisholm correlation']
    VF_CISE = data['Void fraction - CISE correlation']
    VF_DF_bubbly = data['Void fraction - Drift flux model - Bubbly flow']
    VF_DF_plug = data['Void fraction - Drift flux model - Plug flow']
    diagonal = np.arange(0,1.1,0.1)
    
    plt.figure()
    plt.subplots_adjust(right=0.7)
    
    
    plt.plot(VF_measured, VF_homogenous, 'sk ', label='Homogeneous', markersize=6)
    plt.plot(VF_measured, VF_zivi, 'o ',color='orange', label='Zivi', markersize=5)
    plt.plot(VF_measured, VF_chisholm, '^ ',color='grey', label='Chisholm', markersize=5)
    plt.plot(VF_measured, VF_CISE, 'd ',color='green', label='CISE', markersize=5)
    plt.plot(VF_measured, VF_DF_bubbly, 'x ',color='blue', label='Drift flux\nBubbly flow', markersize=5)
    plt.plot(VF_measured, VF_DF_plug, '+ ',color='magenta', label='Drift flux\nPlug flow', markersize=5)
    
    plt.plot(diagonal, diagonal, 'r', label='diagonal')
    plt.plot(diagonal, diagonal*1.2, 'r-.', label='+ 20%')
    plt.plot(diagonal, diagonal*0.8, 'r--', label='- 20%')
    
    plt.grid()
    plt.xlim((0,1))
    plt.ylim((0,1))
    plt.xlabel('Experimental void fraction')
    plt.ylabel('Calculated void fraction')
    
    plt.legend(bbox_to_anchor=(1.04, 0.5), loc="center left")
    
    
if __name__ == '__main__':
    plot_VF()
    plt.show()
    