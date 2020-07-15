##################################
###Lateral Calculation for pile###
##################################

from math import pi
import numpy as np

#input
diameter = 0.5
modulus = 2.e7
inertia = pi * (diamaeter**4) / 64.
pt = 100.
constJ = 0.5
numSegmen = 100
numPoint = 16
stagePt = 10

zo = [0., 3., 6., 11.]
zi = [3., 6., 11., 12.]
gamma = [10., 10., 10., 10.]
cu = [25., 25., 25., 25.]

numData = len(zo)

numNodal = numSegmen + 1

numIndexB = 2 * numNodal

deltaZ = zi[len(zi) - 1] / numSegmen

