import numpy as np
from numpy import polyfit
from math import pi
from operator import truediv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import csv
import timeit


class Pile:

    def __init__(self, pileLength, pileDiameter, topLayer, bottomLayer, gamma, strength, numSegmen=5, numStage=10, load=10):

        self.__pileLength = pileLength
        self.__pileDiameter = pileDiameter
        self.__topLayer = (self.newLayer(topLayer, bottomLayer, gamma, strength, pileLength))[0]
        self.__bottomLayer = (self.newLayer(topLayer, bottomLayer, gamma, strength, pileLength))[1]
        self.__gamma = (self.newLayer(topLayer, bottomLayer, gamma, strength, pileLength))[2]
        self.__strength = (self.newLayer(topLayer, bottomLayer, gamma, strength, pileLength))[3]
        self.__numSegmen = numSegmen
        self.__numStage = numStage
        self.__load = load
        self.constJ = 0.5
        self.modulus = 2.e7
        self.numPoint = 16

    
    @property
    def pileLength(self):
        return self.__pileLength
    
    @pileLength.setter
    def pileLength(self, value):
        if (not isinstance(value, int)) and (not isinstance(value, float)):
            raise TypeError("Pile Length must be in numeric type")
        self.__pileLength = value
    
    @pileLength.deleter
    def pileLength(self):
        del self.__pileLength
    
    @property
    def pileDiameter(self):
        return self.__pileDiameter
    
    @pileDiameter.setter
    def pileDiameter(self, value):
        if (not isinstance(value, int)) and (not isinstance(value, float)):
            raise TypeError("Pile Diameter must be in numeric type")
        self.__pileDiameter = value
    
    @pileDiameter.deleter
    def pileDiameter(self):
        del self.__pileDiameter
    
    @property
    def topLayer(self):
        return self.__topLayer
    
    @topLayer.setter
    def topLayer(self, value):
        if (not isinstance(value, list)) and (not isinstance(value, float)):
            raise TypeError("Top Layer must be in array and numeric type")
        self.__topLayer = value
    
    @topLayer.deleter
    def topLayer(self):
        del self.__topLayer
    
    @property
    def bottomLayer(self):
        return self.__bottomLayer
    
    @bottomLayer.setter
    def bottomLayer(self, value):
        if (not isinstance(value, list)) and (not isinstance(value, float)):
            raise TypeError("Bottom Layer must be in array and numeric type")
        self.__bottomLayer = value
    
    @bottomLayer.deleter
    def bottomLayer(self):
        del self.__bottomLayer
    
    @property
    def gamma(self):
        return self.__gamma
    
    @gamma.setter
    def gamma(self, value):
        if (not isinstance(value, list)) and (not isinstance(value, float)):
            raise TypeError("Gamma must be in array and numeric type")
        self.__gamma = value
    
    @gamma.deleter
    def gamma(self):
        del self.__gamma

    @property
    def strength(self):
        return self.__strength
    
    @strength.setter
    def strength(self, value):
        if (not isinstance(value, list)) and (not isinstance(value, float)):
            raise TypeError("Strength must be in array and numeric type")
        self.__strength = value

    @strength.deleter
    def strength(self):
        del self.__strength

    @property
    def numSegmen(self):
        return self.__numSegmen

    @numSegmen.setter
    def numSegmen(self, value):
        if(not isinstance(value, int)):
            raise TypeError("Number of Nodal must be in integer type")
        self.__numSegmen = value

    @numSegmen.deleter
    def numSegmen(self):
        del self.__numSegmen

    @property
    def numStage(self):
        return self.__numStage
    
    @numStage.setter
    def numStage(self, value):
        if(not isinstance(value, int)):
            raise TypeError("Number of Stage must be in integer type")
        self.__numStage = value
    
    @numStage.deleter
    def numStage(self):
        del self.__numStage

    @property
    def load(self):
        return self.__load
    
    @load.setter
    def load(self, value):
        if (not isinstance(value, int)) and (not isinstance(value, float)):
            raise TypeError("Load must be in integer or float type")
        self.__load = value

    @load.deleter
    def load(self):
        del self.__load
    
    def newLayer(self, topLayer, bottomLayer, gamma, strength, pileLength):
        newBottom = []
        for i in range(len(bottomLayer)):
            if (bottomLayer[i] < pileLength):
                newBottom.append(bottomLayer[i])
            else:
                break
        newBottom.append(pileLength)

        newTop = []
        for i in range(len(newBottom)):
            newTop.append(topLayer[i])
        
        newGamma = []
        for i in range(len(newBottom)):
            newGamma.append(gamma[i])
        
        newStrength = []
        for i in range(len(newBottom)):
            newStrength.append(strength[i])

        return (newTop, newBottom, newGamma, newStrength)

    numNodal = lambda self: 1 + self.numSegmen

    numIndexB = lambda self: 2 * self.numNodal()
    
    deltaZ = lambda self: (self.bottomLayer[(len(self.bottomLayer)) - 1]) / self.numSegmen

    def nDepth(self):
        ndepth = []
        for i in range(self.numNodal()):
            if i == 0:
                ndepthi = 0
            else:
                ndepthi = self.deltaZ() + ndepthi
            ndepth.append(round(ndepthi, 4))
        return ndepth

    def strengthNodal(self):
        ncu = []
        ngamma = []
        ndepth = self.nDepth()
        for i in range(self.numNodal()):
            for j in range(len(self.strength)):
                if i == 0:
                    ncui = self.strength[0]
                    ngammai = self.gamma[0]
                elif i > 0 and i < self.numNodal() - 1:
                    if ndepth[i] > self.topLayer[j] and ndepth[i] < self.bottomLayer[j]:
                        ncui = self.strength[j]
                        ngammai = self.gamma[j]
                else:
                    ncui = self.strength[len(self.strength) - 1]
                    ngammai = self.gamma[len(self.gamma) - 1]
            ncu.append(ncui)
            ngamma.append(ngammai)
        return ncu, ngamma

    def strengthLayer(self):
        cuL = []
        gammaL = []
        for i in range(self.numNodal()):
            ndepth = self.nDepth()
            paramsCu = (self.strengthNodal())[0]
            paramsG = (self.strengthNodal())[1]
            if i == 0:
                tempLayer = ndepth[i + 1] - ndepth[i]
                tempCTimesLayer = paramsCu[i] * tempLayer
                tempGTimesLayer = paramsG[i] * tempLayer
                tempCL = tempCTimesLayer / tempLayer
                tempGL = tempGTimesLayer / tempLayer
            elif i > 0 and i < self.numNodal() - 1:
                tempLayer = tempLayer + (ndepth[i + 1] - ndepth[i])
                tempCTimesLayer = tempCTimesLayer + (paramsCu[i] * (ndepth[i + 1] - ndepth[i]))
                tempGTimesLayer = tempGTimesLayer + (paramsG[i] * (ndepth[i + 1] - ndepth[i]))
                tempCL = tempCTimesLayer / tempLayer
                tempGL = tempGTimesLayer / tempLayer
            else:
                tempCL = paramsCu[len(paramsCu) - 1]
                tempGL = paramsG[len(paramsG) - 1]
            cuL.append(round(tempCL, 2))
            gammaL.append(round(tempGL, 2))
        return cuL, gammaL

    def epsilon50(self, valCu):
        if valCu <= 48.0:
            epsilon50 = 0.02
        elif valCu > 48.0 and valCu < 96.0:
            epsilon50 = 0.01
        else:
            epsilon50 = 0.005
        return epsilon50
    
    def valY50(self, valEps50):
        return (2.5 * valEps50 * self.pileDiameter)

    def valPu(self, valGamma, valCu, valDepth):
        return min(((3.0 + (valGamma * valDepth / valCu) + (self.constJ * valDepth / self.pileDiameter)) * valCu * self.pileDiameter), 9.0 * valCu * self.pileDiameter)
    
    def valP(self, valY, valPu, valY50):
        return (0.5 * valPu * (valY / valY50)**(1 / 3))
    
    def valEiPult(self, valY, valP):
        # from scipy import stats //using python

        x = np.polyfit(valY, valP, 1)
        return (1/x[1]), (1/x[0]) 
        # x = np.array([valY, valP]) //using module scipy
        # r = stats.linregress(x)   //using module scipy
        # return (1/r.intercept), (1/r.slope) //using module scipy

    def calc(self):

        start = timeit.default_timer()

        print('running....')

        if (len(self.topLayer) != len(self.bottomLayer)):
            raise TypeError("Number data top layer and bottom layer not equal")
        
        if (len(self.gamma) != len(self.strength)):
            raise TypeError("Number data gamma and strength not equal")

        numnodal = self.numNodal()
        deltaz = self.deltaZ()
        modulus = self.modulus
        numstage = self.numStage
        load = self.load
        numpoint = self.numPoint
        valLoad = 0
        deltaLoad = load / numstage
        inertia = pi * ((self.pileDiameter)**4) / 64.

        outputValY = []
        elasticValY = []
        for i in range(numstage):
            valLoad = valLoad + deltaLoad
            valC1 = 2.0 * valLoad * (deltaz**3) / (modulus * inertia)

            arrValEi = []
            arrValPult = []
            tempArrValY = []
            tempArrValP = []
            for j in range(self.numNodal()):

                arrValY = []
                arrValP = []
                dy = 0
                for k in range(self.numPoint + 2):
                    cu = (self.strengthLayer())[0]
                    gamma = (self.strengthLayer())[1]
                    depth = self.nDepth()
                    tempValY = dy * self.valY50(self.epsilon50(cu[j]))
                    tempValPu = self.valPu(gamma[j], cu[j], depth[j])
                    if k >= self.numPoint:
                        tempValP = tempValPu
                    else:
                        tempValP = self.valP(tempValY, tempValPu, self.valY50(self.epsilon50(cu[j])))
                    
                    dy = dy + 0.5
                    
                    arrValY.append(tempValY)
                    arrValP.append(tempValP)

                tempArrValY.append(arrValY)
                tempArrValP.append(arrValP)

                arrYperP = list(map(truediv, arrValY[1:-2], arrValP[1:-2]))

                tempEi, tempPult = self.valEiPult(arrValY[1:-2], arrYperP)

                arrValEi.append(tempEi)
                arrValPult.append(tempPult)

            valA = []
            for j in range(numnodal):
                valA.append(arrValEi[j] * (deltaz**4) / (modulus * inertia))
            valA.reverse()
            # print(valA)

            valB = []
            for l in range(self.numIndexB()):
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
                        valB.append(1.0 / (6.0 + valA[m] - valB[2 * m - 4] - valB[2 * m -1] * (4.0 - valB[2 * m -3])))
            # print(valB)

            valD = []
            for n in range(3):
                if n == 0:
                    valD.append(1.0 / valB[2 * (numnodal - 1)])
                elif n == 1:
                    valD.append(valD[0] * valB[2 * (numnodal - 1) + 1] - valB[2 * (numnodal - 1) - 2] * (2.0 - valB[2 * (numnodal - 1) - 3]) - 2.0)
                elif n == 2:
                    valD.append(valD[0] - valB[2 * (numnodal - 1) - 4] - valB[2 * (numnodal - 1) - 1] * (2.0 - valB[2 * (numnodal - 1) - 3]))

            valYi = []
            valYi.append(valC1 * (1.0 + valB[2 * (numnodal - 1) - 2]) / ((valD[2] * (1.0 + valB[2 * (numnodal - 1) - 2])) - (valD[1] * valB[2 * (numnodal - 1) - 1])))
            valYi.append(valB[2 * (numnodal - 1) - 1] * valYi[0] / (1.0 + valB[2 * (numnodal - 1) - 2]))
            valYi.append(valD[0] * valB[2 * (numnodal - 1) + 1] * valYi[1] - valD[0] * valYi[0])

            for j in range(numnodal - 2, -1, -1):
                valYi.insert(0, (-valB[2 * j] * valYi[1] + valB[2 * j + 1] * valYi[0]))
            
            valYi.insert(0, (2.0 * valYi[0] - valYi[1]))
            valYi.insert(0, (valYi[3] - 4 * valYi[2] + 4 * valYi[1]))
            valYi.reverse()
            elasticValY.append(valYi)

            tol = 1.e-5
            iitermax = 50
            listValY = []
            finalY = 0
            Dv = 0.
            for j in range(numnodal):

                tempValYi = valYi[j + 2]
                if (tempValYi <= 0):
                    Pext = max((arrValEi[j] * tempValYi), -(0.95 * arrValPult[j]))
                else:
                    Pext = min((arrValEi[j] * tempValYi), (0.95 * arrValPult[j]))


                iiter = 0
                error = 1.
                while error > tol:
                    iiter += 1


                    if (tempValYi <= 0):
                        Pint = (Dv + tempValYi) / (abs((Dv + tempValYi) / arrValPult[j]) + (1 / arrValEi[j]))
                    else:
                        Pint = (Dv + tempValYi) / (((Dv + tempValYi) / arrValPult[j]) + (1 / arrValEi[j]))


                    valEt = arrValEi[j] * (1 - abs(Pint / arrValPult[j]))**2

                    dy = (Pext - Pint) / valEt

                    Dv = Dv + dy

                    error = abs(Pext - Pint)

                    if iiter == iitermax:
                        break

                finalY = finalY + Dv

                listValY.append(finalY)
                
                Dv = 0
                finalY = 0
                        
            listValY.insert(0, valB[2 * (numnodal - 1) - 1] * listValY[0] / (1.0 + valB[2 * (numnodal - 1) - 2]))
            listValY.insert(0, valD[0] * valB[2 * (numnodal - 1) + 1] * listValY[0] - valD[0] * listValY[1])

            listValY.append(2.0 * listValY[-1] - listValY[-2])
            listValY.append(listValY[-4] - (4.0 * listValY[-3]) + (4.0 * listValY[-2]))
      
            outputValY.append(listValY)

        stop = timeit.default_timer()

        print('time:', str(round(stop - start, 2)) + ' milisec')

        return (outputValY), (elasticValY), (tempArrValY), (tempArrValP)
                
    def show(self):

        deltaz = self.deltaZ()
        dataDepth = self.nDepth()
        dataValY, elasticValY, tempArrValY, tempArrValP = self.calc()
        modulus = self.modulus
        inertia = pi * ((self.pileDiameter)**4) / 64.

        dataDepth.append(dataDepth[-1] + (dataDepth[-1] - dataDepth[-2]))
        dataDepth.append(dataDepth[-1] + (dataDepth[-1] - dataDepth[-2]))
        dataDepth.insert(0, - dataDepth[1])
        dataDepth.insert(0, - dataDepth[3])

        valMoment = []
        valShear = []
        valSoilPressure = []
        for row in elasticValY:
            tempValMoment = []
            tempValShear = []
            tempSoilPressure = []
            for i in range (len(row) - 4):
                tempValMoment.append((modulus * inertia / deltaz**2) * (row[i + 1] - (2 * row[i + 2]) + row[i + 3]))
                tempValShear.append(-(modulus * inertia / (2 * deltaz**3)) * (row[i] - (2 * row[i + 1]) + (2 * row[i + 3]) - row[i + 4]))
                tempSoilPressure.append(-(modulus * inertia / (deltaz**4)) * (row[i] - (4 * row[i + 1]) + (6 * row[i + 2]) - (4 * row[i + 3]) + row[i + 4]))
            valMoment.append(tempValMoment)
            valShear.append(tempValShear)
            valSoilPressure.append(tempSoilPressure)

        valDeflection = []
        for row in dataValY:
            tempValDeflection = []
            for i in range (len(row) - 4):
                tempValDeflection.append(row[i + 2])
            valDeflection.append(tempValDeflection)
            
        data = [(dataDepth[2:-2]), (valDeflection), (valMoment), (valShear), (valSoilPressure)]
        codeLoad = self.load
        numStage = self.numStage
        numSegmen = self.numSegmen
        length = self.pileLength

        fileName = 'Lateral-' + str(codeLoad) + str(numStage) + str(numSegmen) + str(length) + '.csv'

        saveFile = open(fileName, 'w', newline='')
        with saveFile:
            writer = csv.writer(saveFile)
            writer.writerow([fileName])
            writer.writerow(['--Soil Properties--'])
            writer.writerow(['top layer: ' + str(self.topLayer) + ' m'])
            writer.writerow(['bottom layer: ' + str(self.bottomLayer) + ' m'])
            writer.writerow(['unit weight: ' + str(self.gamma) + ' kN/m3'])
            writer.writerow(['strength: ' + str(self.strength) + ' kPa'])
            writer.writerow(['--Pile Properties--'])
            writer.writerow(['diameter: ' + str(self.pileDiameter) + ' m'])
            writer.writerow(['length: ' + str(self.pileLength) + ' m'])
            writer.writerow(['modulus: ' + str(self.modulus) + ' kN/m2'])
            writer.writerow(['--Analysis--'])
            writer.writerow(['maximum load: ' + str(self.load) + ' kN'])
            writer.writerow(['stage number: ' + str(self.numStage)])
            
            writer.writerow(['lateral load (kN) vs lateral deflection (mm)'])
            deltaLoad = codeLoad / numStage
            hload = 0
            for i in range(len(data[1])):
                hload = hload + deltaLoad
                writer.writerow([hload, (data[1][i][0])*1000])
            
            writer.writerow(['lateral deflection (m)'])
            writer.writerow(data[0])
            for i in range(len(data[1])):
                writer.writerows([data[1][i]])
            
            writer.writerow(['moment (kN.m)'])
            writer.writerow(data[0])
            for i in range(len(data[2])):
                writer.writerows([data[2][i]])
            
            writer.writerow(['shear (kN)'])
            writer.writerow(data[0])
            for i in range(len(data[3])):
                writer.writerows([data[3][i]])

            writer.writerow(['soil pressure (kN/m)'])
            writer.writerow(data[0])
            for i in range(len(data[4])):
                writer.writerows([data[4][i]])

            writer.writerow(['--p y curve--'])
            for i in range(len(tempArrValY)):
                writer.writerow(['depth: ' + str(data[0][i]) + ' m'])
                for j in range(len(tempArrValY[i])):
                    writer.writerow([tempArrValY[i][j], tempArrValP[i][j]])

        
        print('done')    
        return (dataDepth[2:-2]), (valDeflection), (valMoment), (valShear), (valSoilPressure)

        # from openpyxl import Workbook
        # import numpy as np

        # book = Workbook()
        # sheet = book.active

        # rows = outputValY

        # datadepth = self.nDepth()

        # datadepth.append(datadepth[-1] + (datadepth[-1] - datadepth[-2]))
        # datadepth.append(datadepth[-1] + (datadepth[-1] - datadepth[-2]))
        # datadepth.insert(0, -datadepth[1])
        # datadepth.insert(0, -datadepth[3])

        # allData = np.append([datadepth], rows, axis=0)

        
        # valMoment = []
        # valShear = []
        # for row in rows:
        #     # print(row)
        #     tempValMoment = []
        #     tempValShear = []
        #     for i in range (len(row)-4):
        #         tempValMoment.append(-(modulus * inertia / deltaz**2) * (row[i + 1] + (2 * row[i + 2]) + row[i + 3]))
        #         tempValShear.append(-(modulus * inertia / (2 * deltaz**3)) * (row[i] - (2 * row[i + 1]) + (2 * row[i + 3]) - row[i + 4]))
        #     valMoment.append(tempValMoment)
        #     valShear.append(tempValShear)

        # print(valMoment)
        # print(valShear)
        
        # sheet.append(datadepth[2:-2])

        # for valMomentIndex in valMoment:
        #     sheet.append(valMomentIndex)    

        # for valShearIndex in valShear:
        #     sheet.append(valShearIndex)

        # for row in rows:
        #     sheet.append(row[2:-2])
        

        # for i in range(len(rows) - 1):
        #     tempValMoment = []
        #     tempValShear = []
        #     for j in range(len(datadepth) - 2):
                
        #         tempValMoment.append(rows[i][j+2])
        #     # valMoment.append(tempValMoment)

        #     sheet.append(tempValMoment)



        # numsegmen = str(self.numSegmen)

        # book.save('lateral' + numsegmen + '.xlsx')
        


def main(): 
    if __name__ == "__main__":
        main()