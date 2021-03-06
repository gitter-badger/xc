# -*- coding: utf-8 -*-
#Test comprobación del cálculo del cortante de agotamiento por
#resistencia a tracción del hormigón (Vu2) en una sección
#SIN reinforcement de cortante según los artículos 44.2.3.2.1.1
#y  44.2.3.2.1.2 de EHE-08.

import sys

from materials.ehe import comprobVEHE08
from materials.ehe import EHE_concrete
import math

fck=25e6
gammac=1.5
concr=EHE_concrete.EHEConcrete('HA',-fck,gammac)
fctd=concr.fctkEHE08()/gammac
fcd=concr.fcd()*(-1)
d=1.45
b0=0.6
I=0.76
S=0.619
alphaL=1.0
NCd=0
Ac=2.3
AsPas=32*3.14e-4
Vu2NoFis=comprobVEHE08.getVu2EHE08NoAtNoFis(fctd,I,S,b0,alphaL,NCd,Ac)
Vu2SiFis=comprobVEHE08.getVu2EHE08NoAtSiFis(fck,fcd,1.5,NCd,Ac,b0,d,AsPas,0.0)
vChi=min(2,1+math.sqrt(200/(d*1000)))
Sgpcd=min(min(NCd/Ac,0.3*fcd),12e6)
Vu2Min=comprobVEHE08.getFcvMinEHE08(fck,1.5,d,vChi,Sgpcd)*b0*d
Vu2A=comprobVEHE08.getVu2EHE08NoAt(1,2,fck,fck,1.5,I,S,alphaL,NCd,Ac,b0,d,AsPas,0.0)
Vu2B=comprobVEHE08.getVu2EHE08NoAt(2,1,fck,fck,1.5,I,S,alphaL,NCd,Ac,b0,d,AsPas,0.0)

ratio1= abs((Vu2NoFis-881.781712e3)/881.781712e3)
ratio2= abs((Vu2SiFis-439233)/439233)
ratio3= abs((Vu2Min-349302)/349302)
ratio4= abs((Vu2A-Vu2NoFis)/Vu2NoFis)
ratio5= abs((Vu2B-Vu2SiFis)/Vu2SiFis)


# print "fctd= ",fctd/1e6," MPa"
# print "Vu2NoFis= ",Vu2NoFis/1e3," kN"
# print "Vu2SiFis= ",Vu2SiFis/1e3," kN"
# print "Vu2Min= ",Vu2Min/1e3," kN"
# print "ratio1= ",ratio1
# print "ratio2= ",ratio2
# print "ratio3= ",ratio3
# print "ratio4= ",ratio4
# print "ratio5= ",ratio5


if (ratio1<1e-5) and (ratio2<1e-5) and (ratio3<1e-5) and (ratio4<1e-5) and (ratio5<1e-5):
    print "test cortante EHE-08 02: ok."
else:
    print "test cortante EHE-08 02: ERROR."
  
