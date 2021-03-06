# -*- coding: utf-8 -*-
# home made test
# Testing hinge development in a cantilever.

import xc_base
import geom
import xc

from materials.perfiles_metalicos.arcelor import perfiles_ipe_arcelor as ipe
from materials import aceros_estructurales as steel

test= xc.ProblemaEF()
preprocessor=  test.getPreprocessor

S275JR= steel.S275JR
S275JR.gammaM= 1.05
epp= S275JR.getDesignElasticPerfectlyPlasticMaterial(preprocessor, "epp")
IPE200= ipe.IPEProfile(S275JR,'IPE_200')
fs3d= IPE200.getFiberSection3d(preprocessor,'epp')

curvM= 0.13
fs3d.setTrialSectionDeformation(xc.Vector([0.0,curvM,0.0]))
fs3d.commitState()
Mp1= fs3d.getStressResultantComponent("Mz")
fs3d.revertToStart()
fs3d.setTrialSectionDeformation(xc.Vector([0.0,0.0,curvM]))
fs3d.commitState()
Mp2= fs3d.getStressResultantComponent("My")

yMax= IPE200.hHalf
zMax= IPE200.bHalf
fyd= S275JR.fyd()

WzplTeor= IPE200.get('Wzpl')
Mp1Teor= WzplTeor*fyd
WyplTeor= IPE200.get('Wypl')
Mp2Teor= WyplTeor*fyd
ratio1= (Mp1Teor-Mp1)/Mp1
ratio2= (Mp2Teor-Mp2)/Mp2

'''
print 'WyplTeor=', WyplTeor
print 'Mp1= ', Mp1, ' Mp1Teor= ', Mp1Teor, ' ratio1= ', ratio1
print 'Mp2= ', Mp2, ' Mp2Teor= ', Mp2Teor, ' ratio2= ', ratio2
'''

import os
fname= os.path.basename(__file__)
if (ratio1<0.1) & (ratio2<0.1):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
