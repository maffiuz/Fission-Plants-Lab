import pandas as pd
import matplotlib.pyplot as plt

def plot_TD_annular_slugchurn():
    data = pd.read_csv('data/taitel_duckler.csv')
    x_line = data['X annular - slug churn']
    y_line = data['Y annular - slug churn']
    
    output = pd.read_csv('data/output.csv')    
    X_coord = output['X coordinate TD map - annular-slugchurn']
    Y_coord = output['Y coordinate TD map - annular-slugchurn']
    labels = output['Label Hewitt-Roberts map']
    
    plt.figure()
    plt.subplots_adjust(bottom=0.17)
    plt.loglog()
    plt.plot(x_line,y_line,'k')
    plt.scatter(X_coord,Y_coord)
    for i, (xi, yi, label) in enumerate(zip(X_coord, Y_coord, labels)):
        plt.annotate(label, (xi, yi), xytext=(5, 5), textcoords='offset points', fontsize=10)
    plt.grid()
    plt.xlim((1e2,1e4))
    plt.ylim((1e-3,5))
    plt.xlabel(r'$\left(\frac{(dp/dz)_l}{(dp/dz)_g}\right)^{1/2}$')
    plt.ylabel(r'$j_g\rho_g^{1/2}[g(\rho_l-\rho_g)\sigma]^{-1/4}$')
    plt.text(1, 0.07, 'Slug churn', fontsize=13, ha='center',color='k')
    plt.text(1e3, 0.7, 'Annular', fontsize=13, ha='center',color='k')
    
    
def plot_TD_slugs_churn():
    data = pd.read_csv('data/taitel_duckler.csv')
    x_line = data['X slug - churn']
    y_line = data['Y slug - churn']
    x_line2 = data['X slug - churn - line2']
    y_line2 = data['Y slug - churn - line 2']
    
    output = pd.read_csv('data/output.csv')    
    X_coord = output['X coordinate TD map - slug-churn']
    Y_coord = output['Y coordinate TD map - slug-churn']
    labels = output['Label Hewitt-Roberts map']
    
    plt.figure()
    plt.subplots_adjust(bottom=0.13)
    plt.semilogx()
    plt.plot(x_line,y_line,'k')
    plt.plot(x_line2,y_line2,'k')
    plt.scatter(X_coord,Y_coord)
    for i, (xi, yi, label) in enumerate(zip(X_coord, Y_coord, labels)):
        plt.annotate(label, (xi, yi), xytext=(5, 5), textcoords='offset points', fontsize=10)
    plt.plot()
    plt.grid()
    plt.xlim((1,1e4))
    plt.ylim((0.5,1))
    plt.xlabel(r'$j(gD)^{-1/2}$')
    plt.ylabel(r'$\alpha$')
    plt.text(1e3, 0.7, 'Slugs', fontsize=13, ha='center',color='k')
    plt.text(200, 0.95, 'Churn flow', fontsize=13, ha='center',color='k')
    
    
def plot_TD_bubbly_slugchurn():
    data = pd.read_csv('data/taitel_duckler.csv')
    x_line = data['X bubbly - slug churn']
    y_line = data['Y bubbly - slug churn']
    
    output = pd.read_csv('data/output.csv')    
    X_coord = output['X coordinate TD map - bubbly-slugchurn']
    Y_coord = output['Y coordinate TD map - bubbly-slugchurn']
    labels = output['Label Hewitt-Roberts map']
    
    plt.figure()
    plt.subplots_adjust(bottom=0.145)
    plt.semilogx()
    plt.plot(x_line,y_line,'k')
    plt.scatter(X_coord,Y_coord)
    for i, (xi, yi, label) in enumerate(zip(X_coord, Y_coord, labels)):
        plt.annotate(label, (xi, yi), xytext=(5, 5), textcoords='offset points', fontsize=10)
    plt.grid()
    plt.xlim((1e-1,1e2))
    plt.ylim((0,6))
    plt.xlabel(r'$j_g\rho_l^{1/2}[g(\rho_l-\rho_g)\sigma]^{-1/4}$')
    plt.ylabel(r'$j_l/j_g$')
    plt.text(0.5, 3.4, 'Bubbles', fontsize=13, ha='center',color='k')
    plt.text(35, 1.5, 'Slugs\nChurn flow', fontsize=13, ha='center',color='k')


if __name__ == '__main__':
    plot_TD_annular_slugchurn()
    plot_TD_slugs_churn()
    plot_TD_bubbly_slugchurn()
    plt.show()
    