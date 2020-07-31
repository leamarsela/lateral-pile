class Pile:

    def __init__(self, pileLength=None, pileDiameter=None, topLayer=None, bottomLayer=None, gamma=None, strength=None, numSegmen=5, numStage=10, load=10):
        self.__pileLength = pileLength
        self.__pileDiameter = pileDiameter
        self.__topLayer = topLayer
        self.__bottomLayer = bottomLayer
        self.__gamma = gamma
        self.__strength = strength
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
    def bottomLayer(sef, value):
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


    def numNodal(self):
        return 1 + self.numSegmen

    def numIndexB(self):
        return 2 * self.numNodal()
    
    def deltaZ(self):
        lastIndex = len(self.bottomLayer)
        lastDepth = self.bottomLayer[lastIndex - 1]
        return (lastDepth / self.numSegmen)

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
        import numpy as np
        from scipy import stats

        x = np.array([valY, valP])
        r = stats.linregress(x)
        return (1/r.intercept), (1/r.slope)

    def run(self):
        from math import pi
        from operator import truediv

        if (len(self.topLayer) != len(self.bottomLayer)):
            raise TypeError("Number data top layer and bottom layer not equal")
        
        if (len(self.gamma) != len(self.strength)):
            raise TypeError("Number data gamma and strength not equal")

        inertia = pi * ((self.pileDiameter)**4) / 64.
        valLoad = 0
        deltaLoad = self.load / self.numStage
        numnodal = self.numNodal()
        deltaz = self.deltaZ()
        modulus = self.modulus

        outputValY = []
        for i in range(self.numStage):
            valLoad = valLoad + deltaLoad
            valC1 = 2.0 * valLoad * (deltaz**3) / (modulus * inertia)

            arrValEi = []
            arrValPult = []
            for j in range(numnodal):
                dy = 0
                arrValY = []
                arrValP = []

                for k in range(self.numPoint):
                    dy = dy + 0.5
                    cu = (self.strengthLayer())[0]
                    gamma = (self.strengthLayer())[1]
                    depth = self.nDepth()
                    tempValY = dy * self.valY50(self.epsilon50(cu[j]))
                    tempValPu = self.valPu(gamma[j], cu[j], depth[j])
                    tempValP = self.valP(tempValY, tempValPu, self.valY50(self.epsilon50(cu[j])))
                    
                    arrValY.append(tempValY)
                    arrValP.append(tempValP)
                
                arrYperP = list(map(truediv, arrValY, arrValP))

                tempEi, tempPult = self.valEiPult(arrValY, arrYperP)

                arrValEi.append(tempEi)
                arrValPult.append(tempPult)

            valA = []
            for j in range(numnodal):
                valA.append(arrValEi[j] * (deltaz**4) / (modulus * inertia))
            valA.reverse()

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

            tol = 1.e-5
            iitermax = 50
            listValY = []
            finalY = 0
            Dv = 0.
            for j in range(numnodal):

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

        print(outputValY)
        print(valYi)
        print(self.nDepth())
        




def main(): 
    if __name__ == "__main__":
        main()