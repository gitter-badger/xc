# -*- coding: utf-8 -*-
# Home made test

import xc_base
import geom
import xc
from model import predefined_spaces
from materials import typical_materials
import math

fy= 2600 # Tensión de cedencia del material expresada en kp/cm2.
E= 2.1e6 # Módulo de Young del material en kp/cm2.
xA= 1/3.0
yA= 3/4.0
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
epp= typical_materials.defElasticPPMaterial(preprocessor, "epp",E,fy,-fy)
geomPrueba= preprocessor.getMaterialLoader.newSectionGeometry("geomPrueba")
geomPrueba.tagSpot= 1
spot1= geomPrueba.newSpot(geom.Pos2d(xA,yA))
x1= spot1.pos.x
y1= spot1.pos.y
spot2= geomPrueba.newSpot(geom.Pos2d(0,0))
spot3= geomPrueba.newSpot(geom.Pos2d(10,10))
dist= geomPrueba.distSpots(1,2)
linea1= geomPrueba.newSegment(2,1)
lengthL1= linea1.getLong()
linea2= geomPrueba.newSegment(1,3)
nl1= spot1.numLines
nl2= spot2.numLines
nl3= spot3.numLines

'''
             \for_each_spot

                 print codigo,",",pos.x,",",pos.y,", nlineas:",nlineas

             \for_each_eje

                 print codigo,",",p1.codigo,",",p2.codigo,",",long

'''




ratio1= ((xA-x1)/xA)
ratio2= ((yA-y1)/yA)
ratio3= (dist-math.sqrt((x1)**2+(y1)**2))
ratio4= (dist-lengthL1)
ratio5= (nl1-2)
ratio6= (nl2-1)
ratio7= (nl3-1)

'''
print "xA= ", xA 
print "x1= ", x1 
print "ratio1= ",ratio1
print "ratio2= ",ratio2
print "ratio3= ",ratio3
'''

import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-12) & (abs(ratio2)<1e-12) & (abs(ratio3)<1e-12) & (abs(ratio4)<1e-12) & (abs(ratio5)<1e-12) & (abs(ratio6)<1e-12) & (abs(ratio7)<1e-12):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
