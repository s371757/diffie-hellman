import matplotlib.pyplot as plt
import numpy as np
from sympy import totient

def visualize_phi_over_n():
    n_values = np.arange(1, 101)
    phi_n_values = np.array([totient(n) for n in n_values]) / n_values
    # Visualisierung
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, phi_n_values, marker='o')
    plt.xlabel('n')
    plt.ylabel('φ(n) / n')
    plt.title('Visualisierung von φ(n) / n')
    plt.grid(True)
    plt.show()


def visualize_phi():
    # Berechnen der Werte von φ(n) für n von 1 bis 100
    phi_values = np.array([totient(n) for n in n_values])

    # Visualisierung
    plt.figure(figsize=(10, 6))
    plt.plot(n_values, phi_values, marker='o', color='green')
    plt.xlabel('n')
    plt.ylabel('φ(n)')
    plt.title('Visualisierung von φ(n)')
    plt.grid(True)
    plt.show()


if __name__ == "__main__":
    visualize_phi()
    visualize_phi_over_n()
