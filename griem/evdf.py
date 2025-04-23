"""
evdf.py
"""

# Import libraries
import numpy as np
import matplotlib.pyplot as plt

from scipy.constants import k as kB, m_e  # Boltzmann constant and electron mass


class EVDF:
    def __init__(self, vels, fv):
        self.vels = vels
        self.fv = fv

    def calc_area(self):
        area = np.trapz(self.fv, self.vels)
        return area

    def calc_v_avg(self):
        return np.trapz(self.fv*vels, self.vels)
    
    def plot(self):
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_xlabel(r"Velocity, $v$")
        ax.set_ylabel(r"EVDF, $f(v)$")
        ax.plot(self.vels, self.fv)
        plt.show()



class Maxwellian(EVDF):
    def __init__(self, vels, temp):
        fv = self._compute_maxwellian(vels, temp)
        super().__init__(vels, fv)

    @staticmethod
    def _compute_maxwellian(vels, temp, m=m_e):

        factor = (m / (2 * np.pi * kB * temp))**1.5
        fv = 4 * np.pi * vels**2 * np.exp(-m * vels**2 / (2 * kB * temp))
        
        # Normalize
        normalization = np.trapz(fv, vels)
        return fv / normalization
