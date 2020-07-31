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
numSegmen = 5
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



# hitung
valPt = 0
deltaPt = pt / stagePt

outputValY = []
for i in range(stagePt):

    valPt = valPt + deltaPt
    valC1 = 2.0 * valPt * (deltaZ**3) / (modulus * inertia)

    arrValEi = []
    arrValPult = []
    for j in range(numNodal):
    
        dy = 0
        arrValY = []
        arrValP = []
        for k in range(numPoint):
            dy = dy + 0.5
            tempValY = dy * y50(epsilon50(cuI[j]))
            tempValPu = valPu(gammaI[j], nDepth[j], cuI[j])
            tempValP = valP(tempValY, tempValPu, y50(epsilon50(cuI[j])))
            
            arrValY.append(tempValY)
            arrValP.append(tempValP)
            

        arrYperP = list(map(truediv, arrValY, arrValP))

        tempEi, tempPult = valEiPult(arrValY, arrYperP)
    
        arrValEi.append(tempEi)
        arrValPult.append(tempPult)


    valA = []
    for j in range(numNodal):
        valA.append(arrValEi[j] * (deltaZ**4) / (modulus * inertia))
    valA.reverse()


    valB = []
    for l in range(numIndexB):
        if l == 0:
            valB.append(2.0 / (valA[0] + 2.0))
        elif l == 1:
            valB.append(2.0 * valB[0])
        elif l == 2:
            valB.append(1.0 / (5.0 + valA[1] - 2.0 * valB[1]))
        else:
            if l % 2 != 0:
                m = (l - 1) // 2
                valB.append(valB[2 * m] * (4.0 - valB[2 * m - 1]))
            elif l % 2 == 0:
                m = l // 2
                valB.append(1.0 / (6.0 + valA[m] - valB[2 * m - 4] - valB[2 * m - 1] * (4.0 - valB[2 * m - 3])))


    valD = []
    for n in range(3):
        if n == 0:
            valD.append(1.0 / valB[2 * (numNodal - 1)])
        elif n == 1:
            valD.append(valD[0] * valB[2 * (numNodal - 1) + 1] - valB[2 * (numNodal - 1) - 2] * (2.0 - valB[2 * (numNodal - 1) - 3]) - 2.0)
        elif n == 2:
            valD.append(valD[0] - valB[2 * (numNodal - 1) - 4] - valB[2 * (numNodal - 1) - 1] * (2.0 - valB[2 * (numNodal - 1) - 3]))


    valYi = []
    valYi.append(valC1 * (1.0 + valB[2 * (numNodal - 1) - 2]) / ((valD[2] * (1.0 + valB[2 * (numNodal - 1) - 2])) - (valD[1] * valB[2 * (numNodal - 1) - 1])))
    valYi.append(valB[2 * (numNodal - 1) - 1] * valYi[0] / (1.0 + valB[2 * (numNodal - 1) - 2]))
    valYi.append(valD[0] * valB[2 * (numNodal - 1) + 1] * valYi[1] - valD[0] * valYi[0])

    for j in range(numNodal - 2, -1, -1):
        valYi.insert(0, (-valB[2 * j] * valYi[1] + valB[2 * j + 1] * valYi[0]))
    
    valYi.insert(0, (2.0 * valYi[0] - valYi[1]))
    valYi.insert(0, (valYi[3] - 4 * valYi[2] + 4 * valYi[1]))
    valYi.reverse()

    # outputValY.append(valYi)
    tol = 1.e-5
    iitermax = 50
    listValY = []
    finalY = 0
    Dv = 0.
    for j in range(numNodal):

        tempValYi = valYi[j + 2]
        Pext = arrValEi[j] * tempValYi
        
        iiter = 0
        error = 1.
        while error > tol:
            iiter += 1

            Dv = Dv + tempValYi

            Pint = Dv / ((Dv / arrValPult[j]) + (1 / arrValEi[j]))

            valEt = arrValEi[j] * (1 - (Pint / arrValPult[j]))**2

            dy = (Pext - Pint) / valEt

            Dv = Dv + dy

            error = abs(Pext - Pint)

            if iiter == iitermax:
                break

        finalY = finalY + Dv

        listValY.append(finalY)
        finalY = 0

    outputValY.append(listValY)


# print(outputValY)
print(valYi)

# print(valC1)
# print(valA)
# print(valB)
# print(valD)












# mencetak kedalam file excel
# from openpyxl import Workbook

# book = Workbook()
# sheet = book.active

# rows = outputValY

# for row in rows:
#     sheet.append(row)

# for row in sheet.iter_rows(min_row=1, min_col=1, max_row=10, max_col=100):
#     for cell in row:
#         print(cell.value, end="")
#     print()


# book.save('test4.xlsx')




# print(tempValPu)
# print(tempValY)
# print(arrValP[0])
# print(arrValY)

# print(arrValEi[0])
# print(arrValPult[0])





# valPt = 0
# deltaPt = pt / stagePt

# outputValY = []

# for i in range(stagePt):

#     valPt = valPt + deltaPt
#     valC1 = 2.0 * valPt * (deltaZ)**3 / (modulus * inertia)

#     kom = []
#     for j in range(numNodal):
#         kom.append()











