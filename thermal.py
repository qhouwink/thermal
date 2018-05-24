
"""
Thermal control system Orpheus
Created on Thu May 24 12:19:43 2018

@author: Q.B. Houwink
"""
eps=[]
alp = []

from matplotlib import pyplot as plt

sigma = 5.67*10**(-8)

#Planet characteristics
planets = ['Earth', 'Venus', 'Jupiter', 'Pluto']
R_planet = [6371,	6052,	69911,	1188]
R_orbit = [11371, 11052,	74911, 6188]
a       =	 [0.30,	0.65,	0.52,	0.16]
T_IR    = [255,	227.00,	109.50,	43.00]
J_s	     = [1367.00,	2613.00,	51.00,	1.22]

F = []
J_a = []
J_IR = []

for i in range(4):
    F.append((R_planet[i]/R_orbit[i])**2)
    J_a.append(J_s[i]*F[-1]*a[i])
    J_IR.append(sigma*T_IR[i]**4)
    
#Spacecraft characteristics
T_s = 293
A_e = 40
A_i = A_e/2
P_diss = 4154
  
#Heat calculations

i = 3
for i in range(4):
    Q_solar = []
    Q_planet = []
    Q_IR_planet=[]
    Q_IR = []
    epslst = []
    alphalst = []
    for j in range(100):
        epsilon = j/100
        epslst.append(epsilon)
        Q_IR_planet.append(epsilon*J_IR[i]*A_i)
        Q_IR.append(epsilon*sigma*A_e*T_s**4)
        alpha = (Q_IR[-1]-Q_IR_planet[-1]-P_diss)/(A_i*(J_s[i]+J_a[i]))
        alphalst.append(alpha)  
    alp.append(alphalst)
fig = plt.figure()
ax = plt.subplot(111)
ax.plot(epslst,alp[0],label=planets[0])
ax.plot(epslst,alp[1], label=planets[1])
ax.plot(epslst,alp[2], label=planets[2])
ax.plot(epslst,alp[3], label=planets[3])
#,alp[2],epslst,alp[3],label=planets)
ax.legend(loc='upper right')
#ax.set_title(planets[i])
ax.set_xlabel('Epsilon')
ax.set_ylabel('Alpha')
ax.set_ylim((0,1))
plt.show()