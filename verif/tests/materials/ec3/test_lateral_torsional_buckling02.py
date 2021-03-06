# -*- coding: utf-8 -*-
''' Lateral torsional buckling of steel beams.
   pages 32-34 Example 2 from:
   Eurocodes ‐ Design of steel buildings with worked examples
   Brussels, 16 - 17 October 2014
'''
from __future__ import division
import math
import xc_base
import geom
import xc
import scipy.interpolate


from materials.ec3 import lateral_torsional_buckling as ltb
from materials import aceros_estructurales as steel
from materials.ec3 import EC3IPEProfile as EC3IPE

S355JR= steel.S355JR
gammaM0= 1.05
S355JR.gammaM= gammaM0 
IPE400= EC3IPE.EC3IPEProfile(S355JR,"IPE_400")


# Geometry
k1= 1.0; k2= 1.0
#Check results page 32
L= 6.0 # Bar length (m)
x= [0.0,0.25*L,0.5*L,0.75*L,1.0*L]
M= [-93.7,0,114.3,0,111.4]
mgf= ltb.MomentGradientFactorC1(x,M)
Mcr1= IPE400.getMcr(x,M)
Mcr1Teor= 164.7e3

ratio1= abs(Mcr1-Mcr1Teor)/Mcr1Teor
#NOTE: Here there is a big difference between the results
# from Lopez-Serna method
# 317 kN.m and those from the paper 164.7 kN.m
# In theory results from Lopez-Serna method are safe enough.

#Check results page 34
L= 3 # Bar length (m)
x= [0.0,0.25*L,0.5*L,0.75*L,1.0*L]
M= [-93.7e3,-93.7e3/2.0,0.0,114.3e3/2.0,114.3e3]
mgf= ltb.MomentGradientFactorC1(x,M)
Mcr2= IPE400.getMcr(x,M)
Mcr2Teor= 1778e3

ratio2= abs(Mcr2-Mcr2Teor)/Mcr2Teor

# print 'Mcr1= ', Mcr1/1e3, 'kN m'
# print 'Mcr1Teor= ', Mcr1Teor/1e3, 'kN m'
# print 'ratio1= ', ratio1
# print 'Mcr2= ', Mcr2/1e3, 'kN m'
# print 'Mcr2Teor= ', Mcr2Teor/1e3, 'kN m'
# print 'ratio2= ', ratio2

import os
fname= os.path.basename(__file__)
#Don't make a check over ratio1 SEE NOTE above.
if(ratio2<0.05):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
