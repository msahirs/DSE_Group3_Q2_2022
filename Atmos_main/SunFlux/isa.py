import math

e = math.e
R = 287.053
baseT= 288.15
baseP= 101325.
baseRho=1.225
g=9.80665
DeltaT=[-0.0065, 0.0, 0.001, 0.0028, 0.0, -0.0028, -0.002, 0.0]
LvlH=[0., 11000., 20000., 32000., 47000.,51000.,71000.,84852.,86000.]

def getT(Told,a,Hnew,Hold):
    return Told + (Hnew-Hold)*a

def getP(Tnew,Told,Pold,a,Hnew,Hold):
    if a==0.0:
        return math.pow(e,(-g/(R*Told))*(Hnew-Hold))*Pold
    else:
        return math.pow((Tnew/Told),-g/(a*R))*Pold

def getRho(Pnew,Tnew):
    return Pnew/(R*Tnew)

def getVals(h,n = 288.15):
    c=0
    pT=baseP
    tT=n
    RhoT=baseRho
    swapT = 0
    if (h > LvlH[0] and h <= LvlH[-1]):
        while not(h > LvlH[c] and h <= LvlH[c + 1]) and c < len(LvlH) - 1:
            swapT = tT
            tT = getT(tT, DeltaT[c], LvlH[c + 1], LvlH[c])
            pT = getP(tT, swapT, pT, DeltaT[c], LvlH[c + 1], LvlH[c])
            c+=1
        swapT = tT
        tT = getT(tT, DeltaT[c], h, LvlH[c])
        pT = getP(tT, swapT, pT, DeltaT[c], h, LvlH[c])
        RhoT = getRho(pT, tT)
    Sound = math.sqrt(1.4*R*tT)

    return pT, tT, RhoT, Sound