import pandas as pd
import matplotlib.pyplot as plt

def plot_TD_annular_slugchurn():
    data = pd.read_csv('data/taitel_duckler.csv')
    x_line = data['X annular - slug churn']
    y_line = data['Y annular - slug churn']
    
    plt.figure()
    plt.loglog()
    plt.plot(x_line,y_line,'k')
    plt.grid()
    plt.xlim((1e-2,1e4))
    plt.ylim((1e-3,10))
    
    
def plot_TD_slugs_churn():
    data = pd.read_csv('data/taitel_duckler.csv')
    x_line = data['X slug - churn']
    y_line = data['Y slug - churn']
    x_line2 = data['X slug - churn - line2']
    y_line2 = data['Y slug - churn - line 2']
    
    plt.figure()
    plt.semilogx()
    plt.plot(x_line,y_line,'k')
    plt.plot(x_line2,y_line2,'k')
    plt.grid()
    plt.xlim((1,1e4))
    plt.ylim((0.5,1))
    
    
def plot_TD_bubbly_slugchurn():
    data = pd.read_csv('data/taitel_duckler.csv')
    x_line = data['X bubbly - slug churn']
    y_line = data['Y bubbly - slug churn']
    
    plt.figure()
    plt.semilogx()
    plt.plot(x_line,y_line,'k')
    plt.grid()
    plt.xlim((1e-1,1e2))
    plt.ylim((0,2.5))


if __name__ == '__main__':
    plot_TD_annular_slugchurn()
    plot_TD_slugs_churn()
    plot_TD_bubbly_slugchurn()
    plt.show()
    