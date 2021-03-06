# -*- coding: utf-8 -*-

from __future__ import division
import xc_base
import geom
import xc
from solution import predefined_solutions
from model import predefined_spaces
from materials import typical_materials
from model import fix_node_6dof

__author__= "Luis C. Pérez Tato (LCPT) and Ana Ortega (AOO)"
__copyright__= "Copyright 2015, LCPT and AOO"
__license__= "GPL"
__version__= "3.0"
__email__= "l.pereztato@gmail.com"


b= 0.4
h= 0.8
nDivIJ= 2
nDivJK= 2
y0= 0
z0= 0
L= 1 # Longitud del elmento expresada en metros.

# Problem type
prueba= xc.ProblemaEF()
preprocessor=  prueba.getPreprocessor
nodes= preprocessor.getNodeLoader
predefined_spaces.gdls_resist_materiales3D(nodes)
nodes.defaultTag= 1 #First node number.
nod= nodes.newNodeXYZ(0.0,0.0,0.0)
nod= nodes.newNodeXYZ(L,0.0,0)

trfs= preprocessor.getTransfCooLoader
lin= trfs.newLinearCrdTransf3d("lin")
lin.xzVector= xc.Vector([0,1,0])

# Materials definition
fy= 275e6 # Tensión de cedencia del acero.
E= 210e9 # Módulo de Young del acero.
acero= typical_materials.defSteel01(preprocessor, "acero",E,fy,0.001)

# Secciones
geomCuadFibras= preprocessor.getMaterialLoader.newSectionGeometry("geomCuadFibras")
y1= h/2.0
z1= b/2.0
regiones= geomCuadFibras.getRegions
acero= regiones.newQuadRegion("acero")
acero.nDivIJ= nDivIJ
acero.nDivJK= nDivJK
acero.pMin= geom.Pos2d(y0-y1,z0-z1)
acero.pMax= geom.Pos2d(y0+y1,z0+z1)
cuadFibras= preprocessor.getMaterialLoader.newMaterial("fiber_section_3d","cuadFibras")
fiberSectionRepr= cuadFibras.getFiberSectionRepr()
fiberSectionRepr.setGeomNamed("geomCuadFibras")
cuadFibras.setupFibers()
fibras= cuadFibras.getFibers()
A= fibras.getSumaAreas


# Elements definition
elementos= preprocessor.getElementLoader
elementos.defaultTransformation= "lin"
elementos.defaultMaterial= "cuadFibras"
beam3d= elementos.newElement("force_beam_column_3d",xc.ID([1,2]));



fuerte= beam3d.getVDirStrongAxisGlobalCoord(0)
debil= beam3d.getVDirWeakAxisGlobalCoord(0)
ratio1= ((fuerte[0])**2+(fuerte[2])**2)
ratio2= ((debil[0])**2+(debil[1])**2)


''' 
print "fuerte: ",fuerte
print "debil: ",debil
print "ratio1= ",ratio1
print "ratio2= ",ratio2
   '''

import os
fname= os.path.basename(__file__)
if (ratio1 < 1e-12) & (ratio2 < 1e-12):
  print "test ",fname,": ok."
else:
  print "test ",fname,": ERROR."

