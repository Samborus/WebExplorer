import matplotlib.pyplot as plt
import numpy as np


def cost_1(z):
    return - np.log(sigmoid(z))

def cost_0(z):
    return - np.log(1 - sigmoid(z))

def sigmoid(z):
    return 1.0 / (1.0 + np.exp(-z))

def vievwer1():
    z = np.arange(-10, 10, 0.1)
    phi_z = sigmoid(z)

    c1 = [cost_1(x) for x in z]
    plt.plot(phi_z, c1, label='J(w) jeśli y=1')

    c0 = [cost_0(x) for x in z]
    plt.plot(phi_z, c0, linestyle='--', label='J(w) jeśli y=0')

    plt.ylim(0.0, 5.1)
    plt.xlim([0, 1])
    plt.xlabel('$\phi$(z)')
    plt.ylabel('J(w)')
    plt.legend(loc='best')
    plt.tight_layout()
    #plt.savefig('./rysunki/03_04.png', dpi=300)
    plt.show()