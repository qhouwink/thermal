from collections import namedtuple
from json_gen import *
import numpy as np
from matplotlib import pyplot as plt


BOLTZMANN = 1.38064852*10**(-23)    # J km-1
PLUTO_SOLAR_DISTANCE = 5906376272   # km
VENUS_SOLAR_DISTANCE = 108208000    # km
SOLAR_FLUX = 63.28 * 10 ** 6        # W/m2


thermal_system_design = namedtuple('thermal_design', 'A_e alpha epsilon')
design  = thermal_system_design(A_e=1,
                                alpha=1,
                                epsilon=1)

# material_database =


class ThermalEnergyBalance(object):

    def __init__(self, starting_design):
        self.design = starting_design

    def _update_design(self, _a_e, _alpha, _epsilon):
        self.design(A_e=_a_e,
                    alpha=_alpha,
                    epsilon=_epsilon)

    def prelim_scatter_plot(self,temp, sbplot, xlabel=True, ylabel=True, yticks=True, xticks=True):

        """
        Thermal control system Orpheus
        Created on Thu May 24 12:19:43 2018

        @author: Q.B. Houwink
        """
        eps = []
        alp = []

        from matplotlib import pyplot as plt

        sigma = 5.67 * 10 ** (-8)

        # Planet characteristics
        planets = ['Earth', 'Venus', 'Jupiter', 'Pluto']
        R_planet = [6371, 6052, 69911, 1188]
        R_orbit = [11371, 11052, 74911, 6188]
        a = [0.30, 0.65, 0.52, 0.16]
        T_IR = [255, 227.00, 109.50, 43.00]
        J_s = [1367.00, 2613.00, 51.00, 1.22]

        F = []
        J_a = []
        J_IR = []

        for i in range(4):
            F.append((R_planet[i] / R_orbit[i]) ** 2)
            J_a.append(J_s[i] * F[-1] * a[i])
            J_IR.append(sigma * T_IR[i] ** 4)

        # Spacecraft characteristics
        # 293
        T_s = temp
        A_e = 80
        A_i = A_e / 2
        P_diss = 4154

        # Heat calculations

        i = 3
        for i in range(4):
            Q_solar = []
            Q_planet = []
            Q_IR_planet = []
            Q_IR = []
            epslst = []
            alphalst = []
            for j in range(100):
                epsilon = j / 100
                epslst.append(epsilon)
                Q_IR_planet.append(epsilon * J_IR[i] * A_i)
                Q_IR.append(epsilon * sigma * A_e * T_s ** 4)
                alpha = (Q_IR[-1] - Q_IR_planet[-1] - P_diss) / (A_i * (J_s[i] + J_a[i]))
                alphalst.append(alpha)
            alp.append(alphalst)
        # fig = plt.figure()
        plt.style.use('ggplot')
        ax = plt.subplot(sbplot)

        ymin, ymax = ax.get_ylim()
        xmin, xmax = ax.get_xlim()
        ratio = (xmax - xmin) / (ymax - ymin)
        # ax.set_aspect(ratio)

        ax.plot(epslst, alp[0], label=planets[0], linestyle='--', linewidth=2, color='black')
        ax.plot(epslst, alp[1], label=planets[1], linestyle=':', linewidth=2, color='black')
        ax.plot(epslst, alp[2], label=planets[2], linestyle='-.',linewidth=2, color='black')
        ax.plot(epslst, alp[3], label=planets[3],linewidth=2, color='black')

        osr_y, osr_x = list(zip(*OSR_))
        ax.scatter(osr_x, osr_y, color='blue', marker='x', label='OSR', linewidth=0.5)

        tef_y, tef_x = list(zip(*TEF_))
        ax.scatter(tef_x, tef_y, color='green', marker='X', label='TEF', linewidth=0.5)
        #
        fat_y, fat_x = list(zip(*FAT_))
        # print(np.delete(np.array(fat_y), np.array(fat_y) == 'int'))
        # fat_y, fat_x = np.delete(np.array(fat_y), np.array(fat_y) == 'int'), np.delete(np.array(fat_x), np.array(fat_y) != 'int')
        ax.scatter(fat_x, fat_y, color='red', label='FAT', linewidth=0.5)

        # ,alp[2],epslst,alp[3],label=planets)
        ax.legend(loc='upper center', bbox_to_anchor=(1.0, 1.05))

        # ax.set_title(planets[i])
        if xlabel is True:
            ax.set_xlabel('Epsilon ($\epsilon$)')
        if ylabel is True:
            ax.set_ylabel('Alpha ($\\alpha$)')
        ax.set_ylim((0, 1))
        ax.set_xlim((0, 1))

        if yticks is not True:
            ax.get_yaxis().set_visible(False)
        if xticks is not True:
            ax.get_xaxis().set_visible(False)

        # plt.show()



if __name__=="__main__":
    energy_balance = ThermalEnergyBalance(design)

    # plt.subplot(1, 2, 1)
    energy_balance.prelim_scatter_plot(283, 211, xlabel=False, xticks=False)

    # plt.subplot(1, 2, 2)
    energy_balance.prelim_scatter_plot(323, 212)

    plt.savefig('test.png', dpi=300)
