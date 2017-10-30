# -*- coding: utf-8 -*-
"""
Created on Sat May 20 11:09:34 2017

@author: zihle
"""

import random as rd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

cargo=[]
for j in range(30):
    lefttime=np.zeros(60)
    cometime=np.zeros(60)
    isgoout=np.zeros(60)
    outpower=np.zeros(60)
    for i in range(60):
        while lefttime[i]<=0 or lefttime[i]>24:
            lefttime[i]=rd.gauss(8,1.33)
        while cometime[i]<=lefttime[i] or cometime[i]>24:
            cometime[i]=rd.gauss(18.5,1.99)
        isgoout[i]=int(round(rd.uniform(0.4,0.9),0))
        outpower[i]=rd.uniform(0.3,0.6)
        cargo.append([lefttime[i],cometime[i],isgoout[i],outpower[i]])
print(cargo)
np.savetxt('cargo.txt',cargo)
