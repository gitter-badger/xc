# -*- coding: utf-8 -*-

import xc_base
import geom
import xc
import math
import os

prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor

puntos= preprocessor.getCad.getPoints
pt1= puntos.newPntIDPos3d(1,geom.Pos3d(1.0,1.0,0.0))
pt2= puntos.newPntIDPos3d(2,geom.Pos3d(2,2,0))
pt3= puntos.newPntIDPos3d(3,geom.Pos3d(0,1,0))

rs= geom.Ref3d3d(pt1.getPos,pt2.getPos,pt3.getPos)

pt4= puntos.newPntIDPos3d(4, rs.getPosGlobal(geom.Pos3d(7, 0, 0)))
pos= pt4.getPos
ratio1= (pos.x-5.9497475)
ratio2= pos.y-5.9497475
ratio3= pos.z


''' 
print "ratio1= ",(ratio1)
print "ratio2= ",(ratio2)
print "ratio3= ",(ratio3)
 '''
import os
fname= os.path.basename(__file__)
if (abs(ratio1)<1e-5) & (abs(ratio2)<1e-5) & (abs(ratio3)<1e-5):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."
