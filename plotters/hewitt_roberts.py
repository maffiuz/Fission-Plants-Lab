import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def plot_HR():
    """Generates Hewitt-Robers Map
    Data is taken directly from the csv
    """
    
    data = pd.read_csv('data/output.csv')
    X_coord = data['X coordinate Hewitt-Roberts map']
    Y_coord = data['Y coordinate Hewitt-Roberts map']
    labels = data['Label Hewitt-Roberts map']

    
    # Creating contour lines
    # Bubble -> Slug
    X_bolla_slug_2 = np.linspace(6000, 25000, 100)
    Y_bolla_slug_2 = 2e11 * X_bolla_slug_2 ** (-2.71)
    
    Y_bolla_slug_3 = np.linspace(10, 90, 100)          
    X_bolla_slug_3 = np.full_like(Y_bolla_slug_3, 6000)  

    # Slug -> Churn
    X_slug_churn_1 = np.linspace(10, 90, 100)
    Y_slug_churn_1 = 0.021 * X_slug_churn_1 ** 1.278

    X_slug_churn_2 = np.linspace(90, 500, 100)
    Y_slug_churn_2 = 0.092 * X_slug_churn_2 ** 0.963

    X_slug_churn_3 = np.linspace(500, 1000, 100)
    Y_slug_churn_3 = 2.18 * X_slug_churn_3 ** 0.4489

    X_slug_churn_4 = np.linspace(1000, 6000, 100)
    Y_slug_churn_4 = 33.4 * X_slug_churn_4 ** 0.051

    # Churn -> Annular
    X_churn_annular_1 = np.linspace(1.3, 10, 100)
    Y_churn_annular_1 = 219 * X_churn_annular_1 ** (-0.399)

    X_churn_annular_2 = np.linspace(10, 50000, 100)
    Y_churn_annular_2 = np.full_like(X_churn_annular_2, 90)  # Y = 90 costante


    # Annular -> Wispy Annular
    Y_annular_wispy_1 = np.linspace(90, 900, 100)
    X_annular_wispy_1 = np.full_like(Y_annular_wispy_1, 1000)

    X_annular_wispy_2 = np.linspace(1000, 1300, 100)
    Y_annular_wispy_2 = 2e-9 * X_annular_wispy_2 ** 3.894

    X_annular_wispy_3 = np.linspace(1300, 3000, 100)
    Y_annular_wispy_3 = 0.439 * X_annular_wispy_3 ** 1.217
    
    # Plots
    plt.figure()
    plt.title('Hewitt-Roberts Map')
    plt.loglog()
    plt.plot(X_bolla_slug_2, Y_bolla_slug_2, 'r', linewidth=2)
    plt.plot(X_bolla_slug_3, Y_bolla_slug_3, 'r', linewidth=2)

    plt.plot(X_slug_churn_1, Y_slug_churn_1, 'r', linewidth=2)
    plt.plot(X_slug_churn_2, Y_slug_churn_2, 'r', linewidth=2)
    plt.plot(X_slug_churn_3, Y_slug_churn_3, 'r', linewidth=2)
    plt.plot(X_slug_churn_4, Y_slug_churn_4, 'r', linewidth=2)

    plt.plot(X_churn_annular_1, Y_churn_annular_1, 'r', linewidth=2)
    plt.plot(X_churn_annular_2, Y_churn_annular_2, 'r', linewidth=2)

    plt.plot(X_annular_wispy_1, Y_annular_wispy_1, 'r', linewidth=2)
    plt.plot(X_annular_wispy_2, Y_annular_wispy_2, 'r', linewidth=2)
    plt.plot(X_annular_wispy_3, Y_annular_wispy_3, 'r', linewidth=2)

    plt.scatter(X_coord,Y_coord)
    
    for i, (xi, yi, label) in enumerate(zip(X_coord, Y_coord, labels)):
        plt.annotate(label, (xi, yi), xytext=(5, 5), textcoords='offset points', fontsize=10)

    plt.ylabel(r'$\rho_G j_G^2$ [Pa]')
    plt.xlabel(r'$\rho_L j_L^2$ [Pa]')
    plt.xlim((1,1e5))
    plt.ylim((1e-2,1e4))
    
    plt.text(5e4, 5, 'Bubbly', fontsize=10, ha='center',color='r')
    plt.text(1000, 9, 'Bubble-Slugs', fontsize=10, ha='center',color='r')
    plt.text(10, 0.1, 'Slugs', fontsize=10, ha='center',color='r')
    plt.text(10, 10, 'Churn', fontsize=10, ha='center',color='r')
    plt.text(100, 1000, 'Annular', fontsize=10, ha='center',color='r')
    plt.text(1e4, 1000, 'Wispy-Annular', fontsize=10, ha='center',color='r')
    plt.grid()
    