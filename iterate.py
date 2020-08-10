pult = 129.47
Ei = 3341.90

def valp(valy):
    return (valy/((valy/pult) + (1/Ei)))


def et(valy):
    return Ei*(1 - valp(valy)/pult)**2


itermax = 25
tol = 1e-5
iterY = []
iterP = []
final = 0.
Dv = 0.
tempValY = 0.
for i in range(30):

    tempValY = tempValY + (0.001)
    pext = min(tempValY * Ei, 0.95*pult)

    error = 1
    iiter = 0
    while error > tol:
        iiter += 1

        dy = (pext - valp(tempValY+Dv)) / et(tempValY+Dv)
        # dy = (pext - valp(final+Dv)) / et(final+Dv)
        Dv += dy

        error = abs(pext - valp(tempValY+Dv))

        if iiter == itermax:
            break
    
    final = final + Dv
    Dv = 0

    i+=1

    iterY.append(final)
    iterP.append(valp(final))

print(iterP)
print(iterY)