##################################
###Lateral Calculation for pile###
##################################

from math import pi
import numpy as np
from scipy import stats
from operator import truediv


#input
diameter = 0.5
modulus = 2.e7
inertia = pi * (diameter**4) / 64.
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

# koordinat titik nodals
nDepth = []
for i in range(numNodal):
    if i == 0:
        nDepthI = 0
    else:
        nDepthI = deltaZ + nDepthI
    nDepth.append(round(nDepthI, 4))

# nilai cu dan gamma setiap titik nodal
nCu = []
nGamma = []
for i in range(numNodal):
    for j in range(len(cu)):
        if i == 0:
            nCuI = cu[0]
            nGammaI = gamma[0]
        elif i > 0 and i < numNodal - 1:
            if nDepth[i] > zo[j] and nDepth[i] < zi[j]:
                nCuI = cu[j]
                nGammaI = gamma[j]
        else:
            nCuI = cu[len(cu) - 1]
            nGammaI = gamma[len(gamma) - 1]
    nCu.append(nCuI)
    nGamma.append(nGammaI)

# nilai cu rata2 dan gamma rata2
cuI = []
gammaI = []
for i in range(numNodal):
    if i == 0:
        tempLayer = nDepth[i + 1] - nDepth[i]
        tempCTimesLayer = nCu[i] * tempLayer
        tempGTimesLayer = nGamma[i] * tempLayer
        tempCuI = tempCTimesLayer / tempLayer
        tempGammaI = tempGTimesLayer / tempLayer
    elif i > 0 and i < numNodal - 1:
        tempLayer = tempLayer + (nDepth[i + 1] - nDepth[i])
        tempCTimesLayer = tempCTimesLayer + (nCu[i] * (nDepth[i + 1] - nDepth[i]))
        tempGTimesLayer = tempGTimesLayer + (nGamma[i] * (nDepth[i + 1] - nDepth[i]))
        tempCuI = tempCTimesLayer / tempLayer
        tempGammaI = tempGTimesLayer / tempLayer
    else:
        tempCuI = nCu[len(nCu) - 1]
        tempGammaI = nGamma[len(nGamma) - 1]
    cuI.append(round(tempCuI, 2))
    gammaI.append(round(tempGammaI, 2))


# fungsi untuk menghitung nilai epsilon50
def epsilon50(valCu):
    if valCu <= 48.0:
        epsilon50 = 0.02
    elif valCu > 48.0 and valCu < 96.0:
        epsilon50 = 0.01
    else:
        epsilon50 = 0.005
    return epsilon50


# fungsi untuk menghitung nilai y50
def y50(valEpsilon50):
    return (2.5 * valEpsilon50 * diameter)


# fungsi untuk menghitung nilai Pu
def valPu(valGamma, valDepth, valCu):
    return min(((3.0 + (valGamma * valDepth / valCu) + (constJ * valDepth / diameter)) * valCu * diameter), 9.0 * valCu * diameter)

# fungsi untuk menghitung nilai P
def valP(valY, valPu, valY50):
    return (0.5 * valPu * (valY / valY50)**(1 / 3))
    

# fungsi untuk menghitung nilai Ei dan Pult
def valEiPult(valY, valP):
    x = np.array([valY, valP])
    r = stats.linregress(x)

    return (1/r.intercept), (1/r.slope)










